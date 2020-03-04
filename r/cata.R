# Cata
# 2020 Ian Dennis Miller

# install.packages("RSQLite")
# install.packages("digest")

library(digest)
library(DBI)


# dbListTables(con)
# df = dbReadTable(con, "6a493bd94026b8ff60fcc1601fdd4ec144a2e82eb46d4b4a973263d89130beb7")

# setRefClass("student", fields = list(name = "character", age = "numeric", GPA = "numeric"))

Cata = setRefClass("Cata",
  fields=list(
    filename="character",
    con="S4"
  ),
  methods=list(
    open = function(filename="~/.cata") {
      con <<- dbConnect(RSQLite::SQLite(), filename)
    },
    create = function(df) {

    },
    read = function(checksum) {
      dbReadTable(con, checksum)
    },
    get_checksum = function(df, params) {
      columns_str = paste(names(df), collapse="")
      params_sorted = params[order(unlist(params))]
      params_str = toJSON(params_sorted)
      hash_str = paste(nrow(df), ncol(df), columns_str, params_str, collapse="")
      checksum = digest(hash_str, algo=c("sha256"), serialize=F)
      return(checksum)
    }
  )
)

student <- setRefClass("student",
  fields=list(
    name="character",
    age="numeric",
    GPA="numeric"
  ),
  methods=list(
    inc_age = function(x) {
      age <<- age + x
    },
    dec_age = function(x) {
      age <<- age - x
    }
  )
)

create = function(df, params=FALSE) {

}

read = function(checksum) {
  dbReadTable(con, checksum)
}


do_test = function() {
  errors = 0
  checksum_good = "6a493bd94026b8ff60fcc1601fdd4ec144a2e82eb46d4b4a973263d89130beb7"
  params = c(lr=0.01, momentum=0.9)


  # test checksum
  if (get_checksum(df, params) != checksum_good) {
    print("ERROR")
    errors = errors + 1
  }
  return(errors)
}

cata = Cata("/tmp/test.cata")

do_test()
