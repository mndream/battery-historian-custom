#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import dominate
from dominate.tags import *

js_str = ''


def create_html(html_file_path='./timeline_chart.html'):
    """
    根据 data.json 构建 HTML 页面
    :param html_file_path: HTML 页面输出位置
    :return: None
    """
    doc = dominate.document(title='LogShow')

    with doc.head:
        # 冗余处理，当无法下载时，需要在同目录下放置两个js库文件
        script(src='https://cdn.bootcdn.net/ajax/libs/jquery/3.6.0/jquery.min.js')
        script(src='./jquery.min.js')
        script(src='https://www.gstatic.com/charts/loader.js')
        script(src='./loader.js')

    # eg = 'creator/echart_gantt.js'
    # egf = get_resource_path(eg)
    # egd = 'creator/echart_gantt_data.js'
    # egdf = get_resource_path(egd)
    # with open(egf, "r+", encoding='UTF-8') as fi, \
    #         open(egdf, "w", encoding='UTF-8') as fo:
    #     old = fi.read()
    #     fo.write("var _rawData = ")
    #     fo.write(get_json_data())
    #     fo.write(";")
    #     fo.write(old)
    # with open(egdf, 'r', encoding='UTF-8') as f:
    #     js = f.read()

    append_js_str("""
  google.charts.load("current", {packages:["timeline","controls"],'language': 'ja'});
  google.charts.setOnLoadCallback(drawChart);
  
  function drawChart() {
  var dashboard = new google.visualization.Dashboard(
    document.getElementById('dashboard')
  );

  var control = new google.visualization.ControlWrapper({
    controlType: 'ChartRangeFilter',
    containerId: 'control',
    options: {
      filterColumnIndex: 2,
      ui: {
        minRangeSize: (60 * 60 * 1000),
        chartType: 'TimeLine',
        chartOptions: {
          width: '100%',
          height: 70,
          chartArea: {
            width: '90%',
            height: '80%'
          },
          hAxis: {
            baselineColor: 'none'
          }
        },
        chartView: {
          columns: [1, 2]
        }
      }
    }
  });

  var chart = new google.visualization.ChartWrapper({
    chartType: 'Timeline',
    containerId: 'chart',
    options: {
      width: '100%',
      height: 600,
      chartArea: {
        width: '100%',
        height: '80%'
      },
      tooltip: {
        isHtml: true
      }
    },
    view: {
      columns: [0, 1, 2]
    }
  });

  var dataTable = new google.visualization.DataTable();
  dataTable.addColumn({ type: 'string', id: 'President' });
  dataTable.addColumn({ type: 'date', id: 'Start' });
  dataTable.addColumn({ type: 'date', id: 'End' });
  dataTable.addRows([
  [ 'Washington', new Date(1789, 3, 30), new Date(1797, 2, 4) ],
  [ 'Adams',      new Date(1797, 2, 4),  new Date(1801, 2, 4) ],
  [ 'Jefferson',  new Date(1801, 2, 4),  new Date(1809, 2, 4) ],
  ]);

  dashboard.bind(control, chart);
  dashboard.draw(dataTable);
}
    """)

    with doc:
        with div():
            attr(id='dashboard', style='width: 100%;')
            with div():
                attr(id='chart', style='width: 100%;')
            with div():
                attr(id='control', style='width: 100%;')
        with script(get_js_str()):
            attr(type='text/javascript')

    # 去掉转义字符串
    doc_str = str(doc)
    doc_str = doc_str.replace('&amp;', '&')
    doc_str = doc_str.replace('&lt;', '<')
    doc_str = doc_str.replace('&gt;', '>')
    doc_str = doc_str.replace('&quot;', '"')

    with open(html_file_path, 'w') as f:
        f.write(doc_str)

    os.startfile(os.path.abspath(html_file_path))


def append_js_str(js_append):
    global js_str
    js_str += js_append


def get_js_str():
    global js_str
    return js_str


if __name__ == '__main__':
    create_html()
