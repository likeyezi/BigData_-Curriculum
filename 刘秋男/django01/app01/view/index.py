import json
from random import randint

from django.shortcuts import render, redirect
import json
from app01.models import InputToClean, Output
from django.db.models import Sum, Count


def index(request):
    # 一到四月销售额
    mount = (
        InputToClean.objects
        .filter(date__month__in=[1, 2, 3, 4])
        .values('date__month')
        .annotate(total_mount=Sum('mount'))
        .order_by('date__month')
    )
    total_mount = []
    for record in mount:
        total_mount.append(record['total_mount'])

    # 全部销售额
    sum_mount = InputToClean.objects.aggregate(total_mount=Sum('mount'))['total_mount']
    sum_mount = "{:.2f}".format(sum_mount)

    # 查询有多少个用户
    id_count = InputToClean.objects.values('id').annotate(id_count=Count('id')).count()

    # 平均销售额
    avg_mount = float(sum_mount) / float(id_count)
    avg_mount = "{:.2f}".format(avg_mount)

    # 统计cname前六
    cname_counts = InputToClean.objects.values('cname').annotate(cname_count=Count('cname')).order_by('-cname_count')[
                   :6]

    cname_top_6 = []
    cname_count = []
    for item in cname_counts:
        cname_top_6.append(item["cname"])
        cname_count.append(item['cname_count'])
        print(f'cname: {item["cname"]}, 数量: {item["cname_count"]}')

    # 统计cname前十
    top_cname_counts = InputToClean.objects.values('cname').annotate(cname_count=Count('cname')).order_by(
        '-cname_count')[:10]
    cname_top10 = []
    cname_count_top10 = []
    for item in top_cname_counts:
        cname_top10.append(item["cname"])
        cname_count_top10.append(item['cname_count'])

    # 总记录数
    record_count = InputToClean.objects.count()

    # 用户分析结果
    output_uesrs = Output.objects.values()
    for item in output_uesrs:
        print(item)

    # 统计用户总消费
    mount_by_id = (
        InputToClean.objects
        .values('id')
        .annotate(total_mount=Sum('mount'))
    )

    # 打印每个 id 对应的统计值
    mount_by_ids={}
    for entry in mount_by_id:
        mount_by_ids.setdefault(entry["id"], entry["total_mount"])


    context = {
        'total_mount': total_mount,
        'sum_mount': sum_mount,
        'id_count': id_count,
        'avg_mount': avg_mount,
        'cname_top_6': cname_top_6,
        'cname_count': cname_count,
        'cname_top10': cname_top10,
        'cname_count_top10': cname_count_top10,
        'record_count': record_count,
        'output_uesrs': output_uesrs,
        'mount_by_ids':mount_by_ids,
    }
    return render(request, 'index.html', context)
