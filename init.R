my_packages <- c("netmeta","dplyr","metafor","tidyverse")
 install_if_missing <- function(p) {
    if(p %in% rownames(installed.packages())==FALSE){
    install.packages(p)}
 }
invisible(sapply(my_packages, install_if_missing))


# install.packages('tidyverse', repos = "http://cran.us.r-project.org")
# import rpy2.robjects as robjects \nprint(robjects.r['version'])
# from rpy2.robjects.packages import importr\nbase = importr('base')\nprint(base._libPaths())
