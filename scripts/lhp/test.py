import datetime


def zabbix_quality(request):
    zapi=zabbix_fiveprovince()
    alerts=zapi.trigger.get(
        output=['triggerid', 'description', 'comments', 'lastchange', 'priority','status'],
        expandDescription='true',
        expandComment='true',
        selectHosts=['name'],
        sortfield="priority",
        only_true="true",
        active=1,
        monitored=1,
    )
    print(alerts)

    data_dic = {'code': '0', 'data': {}}

    for row in alerts:
        if "带宽进出相差大于200M" in row['description'] or "带宽进出相差大于500M" in row['description']:
            city = row['hosts']['name'].split('_')[0]
            name = row['hosts']['name']
            comments = row.get('comments', '字段不存在')
            priority = 'levelATwo' if '带宽进出相差大于200M' in row['description'] else 'levelOne'
            lastchange = datetime.datetime.fromtimestamp(int(row['lastchange']))
            duration = datetime.datetime.now() - lastchange
            lastchange = lastchange + datetime.timedelta(hours=8)
            description = row['description']
            if city not in data_dic['data']:
                data_dic['data'][city] = {"priority": priority,
                                          'datas': [
                                              {'name': name,
                                               'comments': comments,
                                               'priority': priority,
                                               'lastchange': lastchange,
                                               'duration': duration,
                                               'description': description}]}
            else:
                data_dic['data'][city]['priority'] = 'levelOne' if priority != data_dic['data'][city]['priority'] else priority
                data_dic['data'][city]['datas'].append({'name': name,
                                               'comments': comments,
                                               'priority': priority,
                                               'lastchange': lastchange,
                                               'duration': duration,
                                               'description': description})
    return data_dic
