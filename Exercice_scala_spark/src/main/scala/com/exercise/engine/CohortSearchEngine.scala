package com.exercise.engine

import com.exercise.model._
import com.exercise.utils.{SolrConf, SolrConnector}
import com.typesafe.scalalogging.LazyLogging
import org.apache.spark.sql.{Dataset, SparkSession}
import org.apache.spark.sql.functions._

class CohortSearchEngine(spark: SparkSession, solrConf: SolrConf)
    extends LazyLogging {

  private val connector = new SolrConnector(spark, solrConf)

  def runSearch(criteria: SearchCriteria): Long = {

    logger.info("Starting cohort search")

    import spark.implicits._

    // 1️⃣ Charger tous les patients
    val basePatients =
      connector
        .loadCollection("patientAphp")
        .select("id")
        .distinct()
        .as[String]

    // 2️⃣ Appliquer dynamiquement les critères
    val afterCriteria =
      criteria.Criteria.foldLeft(basePatients) { (currentSet, criterion) =>

        val collection = mapResourceToCollection(criterion.Resource)

        val solrFilters = buildSolrFilters(criterion.searchParams)

        val df =
          connector.loadCollection(collection, solrFilters)

        val patientIds =
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

    // 3️⃣ Appliquer Perimeter
    val finalSet =
      if (criteria.Perimeters.nonEmpty)
        applyPerimeter(afterCriteria, criteria.Perimeters)
      else afterCriteria

    val result = finalSet.distinct().count()

    logger.info(s"Cohort result: $result patients")

    result
  }

  // -------------------------
  // Resource → Collection
  // -------------------------
  private def mapResourceToCollection(resource: String): String = {
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
  }

  // -------------------------
  // Traduction searchParams → filtres Solr
  // -------------------------
  private def buildSolrFilters(params: String): Seq[String] = {

    params.split("&").toSeq.map { param =>
      val Array(field, value) = param.split("=")

      if (value.startsWith("ge"))
        s"$field:[${value.stripPrefix("ge")}T00:00:00Z TO *]"
      else if (value.startsWith("gt"))
        s"$field:{${value.stripPrefix("gt")}T00:00:00Z TO *]"
      else if (value.startsWith("le"))
        s"$field:[* TO ${value.stripPrefix("le")}T00:00:00Z]"
      else if (value.startsWith("lt"))
        s"$field:[* TO ${value.stripPrefix("lt")}T00:00:00Z}"
      else
        s"$field:$value"
    }
  }

  // -------------------------
  // Gestion Perimeter
  // -------------------------
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