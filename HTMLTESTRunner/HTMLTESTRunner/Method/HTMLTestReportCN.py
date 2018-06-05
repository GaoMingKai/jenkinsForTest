#__author__ = "kirry"

__author__ = "kirry"
__version__ = "S.S.S.S"




import datetime
import unittest
from xml.sax import saxutils
import sys
import threadpool

# ------------------------------------------------------------------------
# The redirectors below are used to capture output during testing. Output
# sent to sys.stdout and sys.stderr are automatically captured. However
# in some cases sys.stdout is already cached before HTMLTestRunner is
# invoked (e.g. calling logging.basicConfig). In order to capture those
# output, use the redirectors for the cached stream.
#
# e.g.
#   >>> logging.basicConfig(stream=HTMLTestRunner.stdout_redirector)
#   >>>

class OutputRedirector(object):
    """ Wrapper to redirect stdout or stderr """
    def __init__(self, fp):
        self.fp = fp

    def write(self, s):
        self.fp.write(s)

    def writelines(self, lines):
        self.fp.writelines(lines)

    def flush(self):
        self.fp.flush()

stdout_redirector = None
stderr_redirector = None

# ----------------------------------------------------------------------
# Template

class Template_mixin(object):
    """
    Define a HTML template for report customerization and generation.

    Overall structure of an HTML report

    HTML
    +------------------------+
    |<html>                  |
    |  <head>                |
    |                        |
    |   STYLESHEET           |
    |   +----------------+   |
    |   |                |   |
    |   +----------------+   |
    |                        |
    |  </head>               |
    |                        |
    |  <body>                |
    |                        |
    |   HEADING              |
    |   +----------------+   |
    |   |                |   |
    |   +----------------+   |
    |                        |
    |   REPORT               |
    |   +----------------+   |
    |   |                |   |
    |   +----------------+   |
    |                        |
    |   ENDING               |
    |   +----------------+   |
    |   |                |   |
    |   +----------------+   |
    |                        |
    |  </body>               |
    |</html>                 |
    +------------------------+
    """

    STATUS = {
    0: '通过',
    1: '失败',
    2: '跳过',
    }

    DEFAULT_TITLE = 'F-One测试报告'
    DEFAULT_DESCRIPTION = ''
    DEFAULT_TESTER='admin'

    # ------------------------------------------------------------------------
    # HTML Template

    HTML_TMPL = r"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <title>%(title)s</title>
    <meta name="generator" content="%(generator)s"/>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
    <link href="http://libs.baidu.com/bootstrap/3.0.3/css/bootstrap.min.css" rel="stylesheet">
    <script src="http://libs.baidu.com/jquery/2.0.0/jquery.min.js"></script>
    <script src="http://libs.baidu.com/bootstrap/3.0.3/js/bootstrap.min.js"></script>
    %(stylesheet)s
</head>
<body >
<script language="javascript" type="text/javascript">
output_list = Array();

/*level 调整增加只显示通过用例的分类 --Findyou
0:Summary //all hiddenRow
1:Failed  //pt hiddenRow, ft none
2:Pass    //pt none, ft hiddenRow
3:All     //pt none, ft none
*/
function showCase(level) {
    trs = document.getElementsByTagName("tr");
    for (var i = 0; i < trs.length; i++) {
        tr = trs[i];
        id = tr.id;
        if (id.substr(0,2) == 'ft') {
            if (level == 2 || level == 0 ) {
                tr.className = 'hiddenRow';
            }
            else {
                tr.className = '';
            }
        }
        if (id.substr(0,2) == 'pt') {
            if (level < 2) {
                tr.className = 'hiddenRow';
            }
            else {
                tr.className = '';
            }
        }
    }

    //加入【详细】切换文字变化 --Findyou
    detail_class=document.getElementsByClassName('detail');
	//console.log(detail_class.length)
	if (level == 3) {
		for (var i = 0; i < detail_class.length; i++){
			detail_class[i].innerHTML="收起"
		}
	}
	else{
			for (var i = 0; i < detail_class.length; i++){
			detail_class[i].innerHTML="详细"
		}
	}
}

function showClassDetail(cid, count) {
    var id_list = Array(count);
    var toHide = 1;
    for (var i = 0; i < count; i++) {
        //ID修改 点 为 下划线 -Findyou
        tid0 = 't' + cid.substr(1) + '_' + (i+1);
        tid = 'f' + tid0;
        tr = document.getElementById(tid);
        if (!tr) {
            tid = 'p' + tid0;
            tr = document.getElementById(tid);
        }
        id_list[i] = tid;
        if (tr.className) {
            toHide = 0;
        }
    }
    for (var i = 0; i < count; i++) {
        tid = id_list[i];
        //修改点击无法收起的BUG，加入【详细】切换文字变化 --Findyou
        if (toHide) {
            document.getElementById(tid).className = 'hiddenRow';
            document.getElementById(cid).innerText = "详细"
        }
        else {
            document.getElementById(tid).className = '';
            document.getElementById(cid).innerText = "收起"
        }
    }
}

function html_escape(s) {
    s = s.replace(/&/g,'&amp;');
    s = s.replace(/</g,'&lt;');
    s = s.replace(/>/g,'&gt;');
    return s;
}
</script>
%(heading)s
%(report)s
%(ending)s

</body>
</html>
"""
    # variables: (title, generator, stylesheet, heading, report, ending)


    # ------------------------------------------------------------------------
    # Stylesheet
    #
    # alternatively use a <link> for external style sheet, e.g.
    #   <link rel="stylesheet" href="$url" type="text/css">

    STYLESHEET_TMPL = """
<style type="text/css" media="screen">
body        { font-family: Microsoft YaHei,Tahoma,arial,helvetica,sans-serif;padding: 20px; font-size: 80%; }
table       { font-size: 100%; }

/* -- heading ---------------------------------------------------------------------- */
.heading {
    margin-top: 0ex;
    margin-bottom: 1ex;
}

.heading .description {
    margin-top: 4ex;
    margin-bottom: 6ex;
}

/* -- report ------------------------------------------------------------------------ */
#total_row  { font-weight: bold; }
.passCase   { color: #5cb85c; }
.failCase   { color: #d9534f; font-weight: bold; }
.errorCase  { color: #f0ad4e; font-weight: bold; }
.hiddenRow  { display: none; }
.testcase   { margin-left: 2em; }
</style>
"""

    # ------------------------------------------------------------------------
    # Heading
    #

    HEADING_TMPL = """<div class='heading'>
<h1 style="font-family: Microsoft YaHei">%(title)s</h1>
%(parameters)s
<p class='description'>%(description)s</p>
</div>

""" # variables: (title, parameters, description)

    HEADING_ATTRIBUTE_TMPL = """<p class='attribute'><strong>%(name)s : </strong> %(value)s</p>
""" # variables: (name, value)



    # ------------------------------------------------------------------------
    # Report
    #
    # 汉化,加美化效果 --Findyou
    REPORT_TMPL = """
<p id='show_detail_line'>
<a class="btn btn-primary" href='javascript:showCase(0)'>概要 %(passrate)s </a>
<a class="btn btn-danger" href='javascript:showCase(1)'>失败 %(fail)s </a>
<a class="btn btn-success" href='javascript:showCase(2)'>通过 %(Pass)s </a>
<a class="btn btn-info" href='javascript:showCase(3)'>所有 %(count)s </a>
</p>
<table id='result_table' class="table table-condensed table-bordered table-hover">
<colgroup>
<col align='left' />
<col align='right' />
<col align='right' />
<col align='right' />
<col align='right' />
<col align='right' />
</colgroup>
<tr id='header_row' class="text-center success" style="font-weight: bold;font-size: 14px;">
    <td>用例集/测试用例</td>
    <td>总计</td>
    <td>通过</td>
    <td>失败</td>
    <td>跳过</td>
    <td>详细</td>
    <td>截图</td>
</tr>
%(test_list)s
<tr id='total_row' class="text-center active">
    <td>总计</td>
    <td>%(count)s</td>
    <td>%(Pass)s</td>
    <td>%(fail)s</td>
    <td>%(error)s</td>
    <td>通过率：%(passrate)s</td>
</tr>
</table>
""" # variables: (test_list, count, Pass, fail, error ,passrate)

    REPORT_CLASS_TMPL = r"""
<tr class='%(style)s warning'>
    <td>%(desc)s</td>
    <td class="text-center">%(count)s</td>
    <td class="text-center">%(Pass)s</td>
    <td class="text-center">%(fail)s</td>
    <td class="text-center">%(error)s</td>
    <td class="text-center"><a href="javascript:showClassDetail('%(cid)s',%(count)s)" class="detail" id='%(cid)s'>详细</a></td>
    <td class="text-center">
    <select  style="width:100px; class="input" onchange="if(this.value!='')window.open(this.value);this.options[0].selected=true" size="1">
<option value="" selected>错误截图</option>
%(PICTURE_TMPL)s
</select>
</td>
</tr>
""" # variables: (style, desc, count, Pass, fail, error, cid)

    #失败 的样式，去掉原来JS效果，美化展示效果  -Findyou
    REPORT_TEST_WITH_OUTPUT_TMPL = r"""
<tr id='%(tid)s' class='%(Class)s'>
    <td class='%(style)s'><div class='testcase'>%(desc)s</div></td>
    <td colspan='5' align='center'>
    <!--默认收起错误信息 -Findyou
    <button id='btn_%(tid)s' type="button"  class="btn btn-danger btn-xs collapsed" data-toggle="collapse" data-target='#div_%(tid)s'>%(status)s</button>
    <div id='div_%(tid)s' class="collapse">  -->

    <!-- 默认展开错误信息 -Findyou -->
    <button id='btn_%(tid)s' type="button"  class="btn btn-danger btn-xs" data-toggle="collapse" data-target='#div_%(tid)s'>%(status)s</button>
    <div id='div_%(tid)s' class="collapse in">
    <pre align='left'>%(script)s</pre>
    </div>
    </td>
</tr>
""" # variables: (tid, Class, style, desc, status)

    # 通过 的样式，加标签效果  -Findyou
    REPORT_TEST_NO_OUTPUT_TMPL = r"""
<tr id='%(tid)s' class='%(Class)s'>
    <td class='%(style)s'><div class='testcase'>%(desc)s</div></td>
    <td colspan='5' align='center'><span class="label label-success success">%(status)s</span></td>
</tr>
""" # variables: (tid, Class, style, desc, status)

    REPORT_TEST_OUTPUT_TMPL = r"""
%(id)s: %(output)s
""" # variables: (id, output)

    # ------------------------------------------------------------------------
    # ENDING
    #
    # 增加返回顶部按钮  --Findyou
    ENDING_TMPL = """<div id='ending'>&nbsp;</div>
    <div style=" position:fixed;right:50px; bottom:30px; width:20px; height:20px;cursor:pointer">
    <a href="#"><span class="glyphicon glyphicon-eject" style = "font-size:30px;" aria-hidden="true">
    </span></a></div>
    """

    PICTURE_TMPL = "<option value=%(url)s>%(pictureName)s</option>"

# -------------------- The end of the Template class -------------------


TestResult = unittest.TestResult

class _TestResult(TestResult):
    # note: _TestResult is a pure representation of results.
    # It lacks the output and reporting ability compares to unittest._TextTestResult.


    def __init__(self, verbosity=1):
        super(_TestResult,self).__init__()
        self.stdout0 = None
        self.stderr0 = None
        self.success_count = 0
        self.failure_count = 0
        self.skipped_count = 0
        self.verbosity = verbosity
        self.result = []
        #增加一个测试通过率 --Findyou
        self.passrate=float(0)


    def startTest(self, test):
        TestResult.startTest(self, test)
        self.stdout0 = True
        self.stderr0 = sys.stderr
        sys.stderr = stderr_redirector


    def complete_output(self):
        """
        Disconnect output redirection and return buffer.
        Safe to call multiple times.
        """
        if self.stdout0:
            sys.stderr = self.stderr0
            self.stdout0 = None
            self.stderr0 = None
        return None


    def stopTest(self, test):
        # Usually one of addSuccess, addError or addFailure would have been called.
        # But there are some path in unittest that would bypass this.
        # We must disconnect stdout in stopTest(), which is guaranteed to be called.
        self.complete_output()


    def addSuccess(self, test):
        self.success_count += 1
        TestResult.addSuccess(self, test)
        output = self.complete_output()
        self.result.append((0, test, output, ''))



    def addSkip(self, test, reason):
        self.skipped_count+=1
        TestResult.addSkip(self,test,reason)
        self.result.append((0, test, reason, ''))


    def addError(self, test, err):
        self.failure_count += 1
        TestResult.addFailure(self, test, err)
        _, _exc_str = self.failures[-1]
        output = self.complete_output()
        self.result.append((1, test, output, _exc_str))


    def addFailure(self, test, err):
        self.failure_count += 1
        TestResult.addFailure(self, test, err)
        _, _exc_str = self.failures[-1]
        output = self.complete_output()
        self.result.append((1, test, output, _exc_str))



class HTMLTestRunner(Template_mixin):
    """
    """
    def __init__(self,suitCase , stream=sys.stdout, verbosity=1,title=None,description=None,tester=None):
        self.stream = stream
        self.verbosity = verbosity
        self._suitCase = suitCase
        self._results = []
        self.beginTime = datetime.datetime.now()
        if title is None:
            self.title = self.DEFAULT_TITLE
        else:
            self.title = title
        if description is None:
            self.description = self.DEFAULT_DESCRIPTION
        else:
            self.description = description
        if tester is None:
            self.tester = self.DEFAULT_TESTER
        else:
            self.tester = tester

        self.startTime = datetime.datetime.now()

    def poolthread(self,num):
        pl=threadpool.ThreadPool(num)
        req=threadpool.makeRequests(self.run,self._suitCase)
        [pl.putRequest(rep) for rep in req]
        pl.wait()
        self.stopTime = datetime.datetime.now()
        self.generateReport(self._results)
        print('\nTime Elapsed: %s' % (self.stopTime-self.startTime), file=sys.stderr)



    def run(self, test):
        "Run the given test case or test suite."
        suit = unittest.TestSuite()
        suit.addTests(test)
        _result = _TestResult(self.verbosity)
        test(_result)
        self._results.append(_result)



    def sortResult(self, result_list):
        rmap = {}
        classes = []
        for n,t,o,e in result_list:
            cls = t.__class__
            if cls not in rmap:
                rmap[cls] = []
                classes.append(cls)
            rmap[cls].append((n,t,o,e))
        r = [(cls, rmap[cls]) for cls in classes]
        return r

    #替换测试结果status为通过率 --Findyou
    def getReportAttributes(self, result):
        """
        Return report attributes as a list of (name, value).
        Override this to add custom attributes.
        """
        success_count = 0
        failure_count = 0
        skipped_count = 0
        startTime = str(self.startTime)[:19]
        duration = "%.2fs"%(self.stopTime - self.startTime).total_seconds()
        for rs in result:
            success_count += rs.success_count
            failure_count += rs.failure_count
            skipped_count += rs.skipped_count
        status = []
        status.append('共 %s' % (success_count + failure_count +skipped_count))
        if success_count: status.append('通过 %s'    % success_count)
        if failure_count: status.append('失败 %s' % failure_count)
        if skipped_count:   status.append('跳过 %s'   % skipped_count  )
        if status:
            status = '，'.join(status)
            self.passrate = str("%.2f%%" % (float(success_count) / float(success_count + failure_count) * 100))
        else:
            status = 'none'
        return [
            ('测试人员', self.tester),
            ('开始时间',startTime),
            ('合计耗时',duration),
            ('测试结果',status + "，通过率= "+self.passrate),
        ]


    def generateReport(self, result):
        report_attrs = self.getReportAttributes(result)
        generator = 'HTMLTestRunner %s' % __version__
        stylesheet = self._generate_stylesheet()
        heading = self._generate_heading(report_attrs)
        report = self._generate_report(result)
        ending = self._generate_ending()
        output = self.HTML_TMPL % dict(
            title = saxutils.escape(self.title),
            generator = generator,
            stylesheet = stylesheet,
            heading = heading,
            report = report,
            ending = ending,
        )
        self.stream.write(output.encode('utf8'))


    def _generate_stylesheet(self):
        return self.STYLESHEET_TMPL

    #增加Tester显示 -Findyou
    def _generate_heading(self, report_attrs):
        a_lines = []
        for name, value in report_attrs:
            line = self.HEADING_ATTRIBUTE_TMPL % dict(
                    name = saxutils.escape(name),
                    value = saxutils.escape(value),
                )
            a_lines.append(line)
        heading = self.HEADING_TMPL % dict(
            title = saxutils.escape(self.title),
            parameters = ''.join(a_lines),
            description = saxutils.escape(self.description),
            tester= saxutils.escape(self.tester),
        )
        return heading

    #生成报告  --Findyou添加注释
    def _generate_report(self, result):
        rows = []
        success_count = 0
        failure_count = 0
        skipped_count = 0
        cid = 0
        for rs in result:
            success_count+=rs.success_count
            failure_count+=rs.failure_count
            skipped_count+=rs.skipped_count
            sortedResult = self.sortResult(rs.result)
            for cls, cls_results in sortedResult:
                cid+=1
                np = nf = ne = 0
                for n,t,o,e in cls_results:
                    if n == 0 and not o:
                        np += 1
                    elif n == 1:
                        nf += 1
                    else:
                        ne += 1

                if cls.__module__ == "__main__":
                    name = cls.__name__
                else:
                    name = "%s.%s" % (cls.__module__, cls.__name__)
                doc = cls.buzName if cls.buzName else cls.__doc__.strip()
                desc = doc and '%s: %s' % (name, doc) or name
                #获取错误图片
                templist = []
                import os,time
                filepath = os.path.abspath("ErrorPicture")
                filename = cls.__module__.split(".")[-1]
                url = "http://192.168.1.18:8080/job/自动化测试集合/job/ui自动化测试/ws/ErrorPicture/%s/"%filename
                filepath = os.path.join(filepath,filename)
                if os.path.exists(filepath):
                    filelist = os.listdir(filepath)
                    for i in filelist:
                        data = datetime.datetime.strptime(time.ctime(os.stat(os.path.join(filepath,i)).st_atime),"%c")
                        if data>self.beginTime:
                            templist.append(
                                self.PICTURE_TMPL % dict(
                                    url = url+i,
                                    pictureName = i
                                )
                            )
                row = self.REPORT_CLASS_TMPL % dict(
                    style = ne > 0 and 'errorClass' or nf > 0 and 'failClass' or 'passClass',
                    desc = desc,
                    count = np+nf+ne,
                    Pass = np,
                    fail = nf,
                    error = ne,
                    cid = 'c%s' % (cid),
                    PICTURE_TMPL = "\n".join(templist)
                )
                rows.append(row)

                for tid, (n,t,o,e) in enumerate(cls_results):
                    self._generate_report_test(rows, cid, tid, n, t, o, e)


        report = self.REPORT_TMPL % dict(
            test_list = ''.join(rows),
            count = str(success_count+failure_count+skipped_count),
            Pass = str(success_count),
            fail = str(failure_count),
            error = str(skipped_count),
            passrate =self.passrate,
        )
        return report


    def _generate_report_test(self, rows, cid, tid, n, t, o, e):
        if n == 0 and o:
            n = 2
        # e.g. 'pt1.1', 'ft1.1', etc
        has_output = bool(o or e)
        # ID修改点为下划线,支持Bootstrap折叠展开特效 - Findyou
        tid = (n == 0 and 'p' or 'f') + 't%s_%s' % (cid,tid+1)
        name = t.id().split('.')[-1]
        doc = t.shortDescription() or ""
        desc = doc and ('%s: %s' % (name, doc)) or name
        tmpl = has_output and self.REPORT_TEST_WITH_OUTPUT_TMPL or self.REPORT_TEST_NO_OUTPUT_TMPL

        # utf-8 支持中文 - Findyou
        if isinstance(o, str):
            uo = o
        else:
            uo = o
        if isinstance(e, str):
            ue = e
        else:
            ue = e

        script = self.REPORT_TEST_OUTPUT_TMPL % dict(
            id = tid,
            output = saxutils.escape(str(uo)+ue),
        )
        import re
        if "AssertionError" in script:
            message = re.search("(?<=AssertionError: ).*[\s\S]*",script).group().strip()
        elif "Exception" in script:
            message = re.search("(?<=Exception: ).*[\s\S]*",script).group().strip()
        else:
            message = script.split(":")[-1].strip()
        if "Exception" in script or "AssertionError" in script:
            message = script.split(":")[-1].strip()
        row = tmpl % dict(
            tid = tid,
            Class = (n == 0 and 'hiddenRow' or 'none'),
            style = n == 2 and 'errorCase' or (n == 1 and 'failCase' or 'passCase'),
            desc = desc,
            script = message,
            status = self.STATUS[n],
        )
        rows.append(row)
        if not has_output:
            return

    def _generate_ending(self):
        return self.ENDING_TMPL







