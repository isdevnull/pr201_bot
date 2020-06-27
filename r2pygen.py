from rpy2.robjects.packages import SignatureTranslatedAnonymousPackage as STAP


s = """
library("exams")
library("ids")

get_questions <- function(path_to_src, pattern=".Rmd|.Rnw") {
  return(list.files(path_to_src, pattern = pattern, full.names = TRUE))
}

generate <- function(questions_raw, name=random_id(bytes = 4), n_problems=5) {
  q_sample <- sample(questions_raw, n_problems)
  rxm <- exams2pdf(q_sample, name = name, dir = "R/pdf", template = "R/template.tex")
  return(c(name, rxm))
}
"""

rxm = STAP(s, "rexams")
