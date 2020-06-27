library("exams")
library("ids")

# temporary path for current wd: "probability_hse_exams/tests/2018_2019/final/rmd"

# args[1] <- number of problems, args[2] <- path to rmd/rnw documents
args <- commandArgs(TRUE)

get_questions <- function(path_to_src, pattern=".Rmd|.Rnw") {
  return(list.files(path_to_src, pattern = pattern, full.names = TRUE))
}

generate <- function(questions_raw, name=random_id(bytes = 8), n_problems=5) {
  q_sample <- sample(questions_raw, n_problems)
  rxm <- exams2pdf(q_sample, name = name, dir = "pdf", tex = './tex', template = "myplain.tex")
  return(rxm)
}

questions_all <- get_questions(args[2])
questions_all

rxm <- generate(questions_all, n_problems = args[1])
