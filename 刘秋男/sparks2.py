from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import StructType, StructField, DateType, LongType, StringType, IntegerType


### 获取系统运行时间的年与月

import datetime
now = datetime.datetime.now()
if len(str(now.month)) >1:
    base_str = "{0}-{1}"
else:
    base_str = "{0}-0{1}"
time_str = base_str.format(now.year, now.month)
print(time_str)


### 电话RFM数据处理
def transfer_call(spark):
    structType = StructType(
        [StructField("date", DateType()), StructField("phone", LongType()), StructField("desc_num", StringType()),
         StructField("count", IntegerType()), StructField("duration", IntegerType()),StructField("create_date", StringType())])

    structType2 = StructType([StructField("desc_num", StringType()), StructField("insitution", StringType()),
                              StructField("tag", StringType()),StructField("create_date", StringType())])

    call_details = spark.read.option("sep",",").schema(structType) \
    .csv("hdfs://node110:9000/input/dx/db/"+time_str+"/call_details/")
    call_flag = spark.read.option("sep", ",").schema(structType2).csv("hdfs://node110:9000/input/dx/db/"+time_str+"/call_flags/")

    ## 进行数据合并

    call_all_data_df = call_details.join(
        call_flag,
        call_details["desc_num"] == call_flag["desc_num"]
    ).select(
        "date"
        , "phone"
        , call_details["desc_num"]
        , "count"
        , "duration"
        , "insitution"
        , "tag"
    )

    ### RFM 模型
    ### R 最近一次消费 当前数据处理应该在月底，每个月的31
    ### F 表示消费的频率
    ### M 表示消耗的资源

    ### day(日期) 是SQL中计算天数的函数，返回当前月的日子day(2016-12-02)-> 2
    call_diff_data_df = call_all_data_df.selectExpr("*", "31-day(date) as diff_day")

    ### 每个人的，每个标签的RFM值

    call_rmf_init_df = call_diff_data_df.groupBy(["phone","tag"])\
    .agg(
        F.min("diff_day").alias("lastest_date"),
        F.sum("count").alias("total_count"),
        F.sum("duration").alias("total_duration")
    ).select(
        "phone"
        ,"tag"
        ,"lastest_date"
        ,"total_count"
        ,"total_duration"
    )

    avg_call_rmf_df = call_diff_data_df.groupBy("tag").agg(
        F.avg("diff_day").alias("avg_lastest_date"),
        F.avg("count").alias("avg_total_count"),
        F.avg("duration").alias("avg_total_duration")
    ).select(
        F.col("tag").alias("avg_tag"),
        "avg_lastest_date"
        ,"avg_total_count"
        ,"avg_total_duration"
    )
    call_rmf_all_df = call_rmf_init_df.join(avg_call_rmf_df, call_rmf_init_df["tag"]==avg_call_rmf_df["avg_tag"]) \
    .select(
        "phone"
        ,"tag"
        ,"lastest_date"
        ,"total_count"
        ,"total_duration"
        ,F.when(F.col("lastest_date")<=F.col("avg_lastest_date"), 1).otherwise(0).alias("flag_days")
        , F.when(F.col("total_count") >= F.col("avg_total_count"), 1).otherwise(0).alias("flag_counts")
        , F.when(F.col("total_duration") >= F.col("avg_total_duration"), 1).otherwise(0).alias("flag_duration")
    )
    return call_rmf_all_df

### 短信RFM数据处理
def transfer_sms(spark):
    structType = StructType(
        [StructField("date", DateType()), StructField("phone", LongType()), StructField("desc_num", StringType()),
         StructField("count", IntegerType()),StructField("create_date", StringType())])

    structType2 = StructType([StructField("desc_num", StringType()), StructField("insitution", StringType()),
                              StructField("tag", StringType()),StructField("create_date", StringType())])

    sms_details = spark.read.option("sep", "\\t").schema(structType) \
        .csv("hdfs://node110:9000/input/dx/db/"+time_str+"/sms_details/")
    sms_flag = spark.read.option("sep", "\\t").schema(structType2).csv("hdfs://node110:9000/input/dx/db/"+time_str+"/sms_flags/")

    ## 进行数据合并

    sms_all_data_df = sms_details.join(
        sms_flag,
        sms_details["desc_num"] == sms_flag["desc_num"]
    ).select(
        "date"
        , "phone"
        , sms_details["desc_num"]
        , "count"
        , "count"
        , "insitution"
        , "tag"
    )

    ### RFM 模型
    ### R 最近一次消费 当前数据处理应该在月底，每个月的31
    ### F 表示消费的频率
    ### M 表示消耗的资源

    ### day(日期) 是SQL中计算天数的函数，返回当前月的日子day(2016-12-02)-> 2
    sms_diff_data_df = sms_all_data_df.selectExpr("*", "31-day(date) as diff_day")

    ### 每个人的，每个标签的RFM值
    sms_rmf_init_df = sms_diff_data_df.groupBy(["phone", "tag"]) \
        .agg(
        F.min("diff_day").alias("lastest_date"),
        F.sum("count").alias("total_count"),
        F.sum("count").alias("total_duration")
    ).select(
        "phone"
        , "tag"
        , "lastest_date"
        , "total_count"
        , "total_duration"
    )

    avg_sms_rmf_df = sms_diff_data_df.groupBy("tag").agg(
        F.avg("diff_day").alias("avg_lastest_date"),
        F.avg("count").alias("avg_total_count"),
        F.avg("count").alias("avg_total_duration")
    ).select(
        F.col("tag").alias("avg_tag"),
        "avg_lastest_date"
        , "avg_total_count"
        , "avg_total_duration"
    )
    sms_rmf_all_df = sms_rmf_init_df.join(avg_sms_rmf_df, sms_rmf_init_df["tag"] == avg_sms_rmf_df["avg_tag"]) \
        .select(
        "phone"
        , "tag"
        , "lastest_date"
        , "total_count"
        , "total_duration"
        , F.when(F.col("lastest_date") <= F.col("avg_lastest_date"), 1).otherwise(0).alias("flag_days")
        , F.when(F.col("total_count") >= F.col("avg_total_count"), 1).otherwise(0).alias("flag_counts")
        , F.when(F.col("total_duration") >= F.col("avg_total_duration"), 1).otherwise(0).alias("flag_duration")
    )
    return sms_rmf_all_df

### 应用RFM数据处理
def transfer_app(spark):
    structType = StructType(
        [StructField("date", DateType()), StructField("phone", LongType()), StructField("desc_num", StringType()),
         StructField("count", IntegerType()), StructField("duration", IntegerType()),StructField("create_date", StringType())])

    structType2 = StructType([StructField("desc_num", StringType()), StructField("insitution", StringType()),
                              StructField("tag", StringType()),StructField("create_date", StringType())])

    app_details = spark.read.option("sep","\\t").schema(structType) \
    .csv("hdfs://node110:9000/input/dx/db/"+time_str+"/app_details/")
    app_flag = spark.read.option("sep", "\\t").schema(structType2).csv("hdfs://node110:9000/input/dx/db/"+time_str+"/app_flags/")

    ## 进行数据合并

    app_all_data_df = app_details.join(
        app_flag,
        app_details["desc_num"] == app_flag["desc_num"]
    ).select(
        "date"
        , "phone"
        , app_details["desc_num"]
        , "count"
        , "duration"
        , "insitution"
        , "tag"
    )

    ### RFM 模型
    ### R 最近一次消费 当前数据处理应该在月底，每个月的31
    ### F 表示消费的频率
    ### M 表示消耗的资源

    ### day(日期) 是SQL中计算天数的函数，返回当前月的日子day(2016-12-02)-> 2
    app_diff_data_df = app_all_data_df.selectExpr("*", "31-day(date) as diff_day")

    ### 每个人的，每个标签的RFM值

    app_rmf_init_df = app_diff_data_df.groupBy(["phone","tag"])\
    .agg(
        F.min("diff_day").alias("lastest_date"),
        F.sum("count").alias("total_count"),
        F.sum("duration").alias("total_duration")
    ).select(
        "phone"
        ,"tag"
        ,"lastest_date"
        ,"total_count"
        ,"total_duration"
    )

    avg_app_rmf_df = app_diff_data_df.groupBy("tag").agg(
        F.avg("diff_day").alias("avg_lastest_date"),
        F.avg("count").alias("avg_total_count"),
        F.avg("duration").alias("avg_total_duration")
    ).select(
        F.col("tag").alias("avg_tag"),
        "avg_lastest_date"
        ,"avg_total_count"
        ,"avg_total_duration"
    )
    app_rmf_all_df = app_rmf_init_df.join(avg_app_rmf_df, app_rmf_init_df["tag"]==avg_app_rmf_df["avg_tag"]) \
    .select(
        "phone"
        ,"tag"
        ,"lastest_date"
        ,"total_count"
        ,"total_duration"
        ,F.when(F.col("lastest_date")<=F.col("avg_lastest_date"), 1).otherwise(0).alias("flag_days")
        , F.when(F.col("total_count") >= F.col("avg_total_count"), 1).otherwise(0).alias("flag_counts")
        , F.when(F.col("total_duration") >= F.col("avg_total_duration"), 1).otherwise(0).alias("flag_duration")
    )
    return app_rmf_all_df

if __name__ == "__main__":

    spark = SparkSession.builder.appName("pri").master("local[*]").getOrCreate()
    sc = spark.sparkContext
    call_RMF_df = transfer_call(spark)
    sms_RMF_df = transfer_sms(spark)
    app_RMF_df = transfer_app(spark)

    ### 联合三张表
    total_RMF_total = call_RMF_df.union(sms_RMF_df).union(app_RMF_df)

    total_RMF_total_01 = total_RMF_total.groupBy(["phone", "tag"]) \
        .agg(
        F.sum("flag_days").alias("flag_days"),
        F.sum("flag_counts").alias("flag_counts"),
        F.sum("flag_duration").alias("flag_duration"),
    )

    # total_RMF_total_01.show(10)
    total_RMF_total_02 = total_RMF_total_01.select(
        "phone"
        , "tag"
        , F.when(F.col("flag_days") > 0, 1).otherwise(0).alias("flag_days")
        , F.when(F.col("flag_counts") > 0, 1).otherwise(0).alias("flag_counts")
        , F.when(F.col("flag_duration") >= 0, 1).otherwise(0).alias("flag_duration")
    )
    total_RMF_total_03 = total_RMF_total_02.withColumn("condition1", F.col("flag_days") + F.col("flag_counts") + F.col(
        "flag_duration")) \
        .withColumn("condition2", F.col("flag_duration"))

    total_RMF_final = total_RMF_total_03.filter(
        "condition1>1 or condition2=1"
    )

    # total_RMF_final.show(100)

    total_RMF_final.createOrReplaceTempView("final")

    sql = """
        select *,'{0}' as create_time from (
            select phone,
                max(case when tag='购物' then 1 else 0 end) as is_shopping,
                max(case when tag='健身' then 1 else 0 end) as is_health,
                max(case when tag='教育' then 1 else 0 end) as is_education,
                max(case when tag='金融理财' then 1 else 0 end) as is_finance,
                max(case when tag='旅游' then 1 else 0 end) as is_touring,
                max(case when tag='美食' then 1 else 0 end) as is_eating,
                max(case when tag='母婴' then 1 else 0 end) as is_baby,
                max(case when tag='医疗' then 1 else 0 end) as is_medical
            from final group by phone
        )
        """.format(time_str)
    print(sql)
    # spark.sql(sql).write.mode("append"). \
    #     format("jdbc"). \
    #     option("url", "jdbc:mysql://node110:3306/dx_sys?useUnicode=true&characterEncoding=utf8&useSSL=false&useUnicode=true"). \
    #     option("dbtable", "dx_analisy"). \
    #     option("user", "root"). \
    #     option("password", "root"). \
    #     save()
    spark.sql(sql).show()




