$(window).load(function () {
    $(".loading").fadeOut()
})

/****/
/****/
$(document).ready(function () {
    var whei = $(window).width()
    $("html").css({fontSize: whei / 20})
    $(window).resize(function () {
        var whei = $(window).width()
        $("html").css({fontSize: whei / 20})
    });
});

$(function () {

    echarts_1();
    echarts_2();
    echarts_3();

    function echarts_1() {
        var myChart = echarts.init(document.getElementById('echart1'));


        for (var i = 0; i < total_mount.length; i++) {
            total_mount[i] = parseFloat(total_mount[i]).toFixed(2);
        }

        // 打印处理后的列表
        console.log(total_mount);
        console.log(cname_top_6);
        console.log(cname_count);


        option = {
            tooltip: {

                trigger: 'axis',
                axisPointer: {
                    lineStyle: {
                        color: '#57617B'
                    }
                },
                formatter: '{b}日	:<br/> 销售情况{c}'
            },

            grid: {
                left: '0',
                right: '20',
                top: '10',
                bottom: '0',
                containLabel: true
            },
            xAxis: [{
                type: 'category',
                boundaryGap: false,
                axisLine: {
                    show: false,
                    lineStyle: {
                        color: 'rgba(255,255,255,.6)'
                    }
                },
                data: ['一月', '二月', '三月', '四月']
            }],
            yAxis: [{
                axisLabel: {
                    show: true,
                    textStyle: {
                        color: 'rgba(255,255,255,.6)'
                    }
                },
                axisLine: {
                    show: false,

                },
                splitLine: {
                    lineStyle: {
                        type: 'dotted',
                        color: 'rgba(255,255,255,.1)'
                    }
                }
            }],
            series: [{
                name: '生产情况',
                type: 'line',
                smooth: true,
                symbol: 'circle',
                symbolSize: 5,
                showSymbol: false,
                lineStyle: {
                    normal: {
                        width: 2
                    }
                },

                areaStyle: {
                    normal: {
                        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                            offset: 0,
                            color: 'rgba(98, 201, 141, 0.5)'
                        }, {
                            offset: 1,
                            color: 'rgba(98, 201, 141, 0.1)'
                        }], false),
                        shadowColor: 'rgba(0, 0, 0, 0.1)',
                        shadowBlur: 10
                    }
                },
                itemStyle: {
                    normal: {
                        color: '#4cb9cf',
                        borderColor: 'rgba(98, 201, 141,0.27)',
                        borderWidth: 12
                    }
                },
                data: total_mount
            }]
        };

        // 使用刚指定的配置项和数据显示图表。
        myChart.setOption(option);
        window.addEventListener("resize", function () {
            myChart.resize();
        });
    }

    function echarts_2() {
        // 基于准备好的dom，初始化echarts实例
        var myChart = echarts.init(document.getElementById('echart2'));

        option = {
            tooltip: {
                trigger: 'axis'
            },
            radar: {
                indicator: [{
                    name: cname_top_6[0],
                    max: 11000,
                    num: cname_count[0],
                }, {
                    name: cname_top_6[1],
                    max: 11000,
                    num: cname_count[1],
                }, {
                    name: cname_top_6[2],
                    max: 11000,
                    num: cname_count[2],
                }, {
                    name: cname_top_6[3],
                    max: 11000,
                    num: cname_count[3],
                }, {
                    name: cname_top_6[4],
                    max: 11000,
                    num: cname_count[4],
                }, {
                    name: cname_top_6[5],
                    max: 11000,
                    num: cname_count[5],
                }],
                splitNumber: 4,
                nameGap: 0,
                axisLine: { //指向外圈文本的分隔线样式
                    lineStyle: {
                        color: '#2c353d'
                    }
                },
                splitLine: {
                    lineStyle: {
                        color: ['#2c353d'],
                        width: 1
                    }
                },
                splitArea: {
                    areaStyle: {
                        color: ['transparent']
                    }
                },
                name: {
                    color: 'rgba(255,255,255,.8)',

                },
            },
            series: [{
                type: 'radar',
                tooltip: {
                    trigger: 'item'
                },
                symbol: 'none',
                itemStyle: {
                    normal: {
                        color: '#096e32',
                        borderColor: '#46ff91'
                    }
                },
                areaStyle: {
                    color: ['#096e32'],
                    opacity: 0.4
                },
                data: [{
                    value: cname_count,
                }]
            },]
        };
        // 使用刚指定的配置项和数据显示图表。
        myChart.setOption(option);
        window.addEventListener("resize", function () {
            myChart.resize();
        });
    }

    function echarts_3() {
        var myChart = echarts.init(document.getElementById('echart3'));
        option = {
            tooltip: {

                trigger: 'axis',
                axisPointer: {
                    lineStyle: {
                        color: '#57617B'
                    }
                },
                formatter: '{b}:<br/> 产量统计{c}'
            },

            grid: {
                left: '0',
                right: '20',
                top: '10',
                bottom: '0',
                containLabel: true
            },
            xAxis: [{
                type: 'category',
                boundaryGap: false,
                axisLabel: {
                    interval: 0, // 设置标签全部展示
                    textStyle: {
                        color: 'rgba(255,255,255,.6)'
                    }
                },
                data: cname_top10
            }],
            yAxis: [{
                axisLabel: {
                    show: true,
                    textStyle: {
                        color: 'rgba(255,255,255,.6)'
                    }
                },
                axisLine: {
                    show: false,

                },
                splitLine: {
                    lineStyle: {
                        type: 'dotted',
                        color: 'rgba(255,255,255,.1)'
                    }
                }
            }],
            series: [{
                name: '产量统计',
                type: 'bar',
                //smooth: true,
                symbol: 'circle',
                symbolSize: 5,
                barWidth: '10%',
                //showSymbol: false,
                lineStyle: {
                    normal: {
                        width: 2
                    }
                },

                areaStyle: {
                    normal: {
                        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                            offset: 0,
                            color: 'rgba(98, 201, 141, 0.5)'
                        }, {
                            offset: 1,
                            color: 'rgba(98, 201, 141, 0.1)'
                        }], false),
                        shadowColor: 'rgba(0, 0, 0, 0.1)',
                        shadowBlur: 10
                    }
                },
                itemStyle: {
                    normal: {
                        color: '#4cb9cf',
                        borderColor: 'rgba(98, 201, 141,0.27)',
                        borderWidth: 12
                    }
                },
                data: cname_count_top10
            }]
        };

        // 使用刚指定的配置项和数据显示图表。
        myChart.setOption(option);
        window.addEventListener("resize", function () {
            myChart.resize();
        });
    }
})












