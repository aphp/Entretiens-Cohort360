package com.exercise.engine

import com.exercise.model._
import com.exercise.utils.{SolrConf, SolrConnector}
import com.typesafe.scalalogging.LazyLogging
import org.apache.spark.sql.{Dataset, SparkSession}
import org.apache.spark.sql.functions._

class CohortSearchEngine(
    spark: SparkSession,
    solrConf: SolrConf
) extends LazyLogging {

  private val connector = new SolrConnector(spark, solrConf)

  def runSearch(criteria: SearchCriteria): Long = {

    logger.info("Starting cohort search")
    import spark.implicits._

    // 1️⃣ Charger tous les patients de base
    val basePatients: Dataset[String] =
      connector
        .loadCollection("patientAphp")
        .select("id")
        .distinct()
        .as[String]

    // 2️⃣ Appliquer dynamiquement tous les critères
    val afterCriteria =
      criteria.Criteria.foldLeft(basePatients) { (currentSet, criterion) =>

        val collection = mapResourceToCollection(criterion.Resource)
        val solrFilters = buildSolrFilters(criterion.searchParams)

        val df = connector.loadCollection(collection, solrFilters)

        val patientIds: Dataset[String] =
          if (criterion.Resource == "Patient") {
            df.select("id").distinct().as[String]
          } else {
            df
              .select(
                regexp_replace(
                  col("subject.reference"),
                  "Patient/",
                  ""
                ).alias("patientId")
              )
              .distinct()
              .as[String]
          }

        if (criterion.Include == "true")
          currentSet.intersect(patientIds)
        else
          currentSet.except(patientIds)
      }

    // 3️⃣ Appliquer les Perimeters
    val finalSet =
      if (criteria.Perimeters.nonEmpty)
        applyPerimeter(afterCriteria, criteria.Perimeters)
      else afterCriteria

    val result = finalSet.distinct().count()

    logger.info(s"Cohort result: $result patients")
    result
  }

  // -------------------------------------------------
  // Mapping Resource → Collection Solr
  // -------------------------------------------------
  private def mapResourceToCollection(resource: String): String =
    resource match {
      case "Patient"           => "patientAphp"
      case "Encounter"         => "encounterAphp"
      case "DocumentReference" => "documentReferenceAphp"
      case "Organization"      => "organizationAphp"
      case other =>
        throw new IllegalArgumentException(
          s"Unknown resource: $other"
        )
    }

  // -------------------------------------------------
  // Traduction FHIR searchParams → filtres Solr
  // -------------------------------------------------
  private def buildSolrFilters(params: String): Seq[String] = {

    if (params == null || params.trim.isEmpty) return Seq.empty

    params.split("&").toSeq.flatMap { param =>
      param.split("=", 2) match {
        case Array(field, value) => Some(buildSingleFilter(field, value))
        case _                   => None
      }
    }
  }

  private def buildSingleFilter(field: String, value: String): String = {

    def isDate(v: String): Boolean =
      v.matches("""\d{4}-\d{2}-\d{2}""")

    if (value.startsWith("ge"))
      buildRangeFilter(field, value.stripPrefix("ge"), ">=")
    else if (value.startsWith("gt"))
      buildRangeFilter(field, value.stripPrefix("gt"), ">")
    else if (value.startsWith("le"))
      buildRangeFilter(field, value.stripPrefix("le"), "<=")
    else if (value.startsWith("lt"))
      buildRangeFilter(field, value.stripPrefix("lt"), "<")
    else
      s"$field:$value"
  }

  private def buildRangeFilter(
      field: String,
      rawValue: String,
      operator: String
  ): String = {

    val isDate = rawValue.matches("""\d{4}-\d{2}-\d{2}""")

    val formattedValue =
      if (isDate) s"${rawValue}T00:00:00Z"
      else rawValue

    operator match {
      case ">=" => s"$field:[$formattedValue TO *]"
      case ">"  => s"$field:{$formattedValue TO *]"
      case "<=" => s"$field:[* TO $formattedValue]"
      case "<"  => s"$field:[* TO $formattedValue}"
    }
  }

  // -------------------------------------------------
  // Gestion Perimeter
  // -------------------------------------------------
  private def applyPerimeter(
      currentPatients: Dataset[String],
      perimeters: Seq[String]
  ): Dataset[String] = {

    import spark.implicits._

    val encounterDf =
      connector.loadCollection(
        "encounterAphp",
        perimeters.map(p => s"serviceProvider.reference:$p")
      )

    val allowedPatients =
      encounterDf
        .select(
          regexp_replace(
            col("subject.reference"),
            "Patient/",
            ""
          ).alias("patientId")
        )
        .distinct()
        .as[String]

    currentPatients.intersect(allowedPatients)
  }

  def stop(): Unit = spark.stop()
}