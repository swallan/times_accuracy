args <- commandArgs(trailingOnly=TRUE)
options(digits=22)
options(warn=-1)

# test if there is at least one argument: if not, return an error
if (length(args)<=2) {
  stop("The arguments <q>, <k>, <df> must be provided.", call.=FALSE)
}

start.time <- Sys.time()
res <- ptukey(as.numeric(args[1]), nmeans = as.numeric(args[2]), df = as.numeric(args[3]))
end.time <- Sys.time()
time.taken <- end.time - start.time
sprintf("%.22g,%.22g", res, time.taken)
