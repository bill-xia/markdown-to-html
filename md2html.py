filename = '弧长';
'''
This parser recognizes:
- headings
- unordered list
- ordered list
- quote
- code block
- paragraph
- inline code
- bold
- italic
- bold-italic
- picture
- link
- math formula
'''
'''
bugs:
line 147
line 179
'''
import re

def buildtree(file):
    tree = [];
    while(file.strip() != ''):
        for pat in pattern:
            res = re.match(pat, file);
            if(res == None):
                continue;
            cont = [];
            if(res.groups()[0].strip() != ''):
                cont.append(res.groups()[0]);
            file = res.groups()[1];
            if(pat == r'(\|.*?\n)([\s\S]*)'):
                while(True):
                    res = re.match(pat, file);
                    if(res == None):
                        break;
                    if(res.groups()[0].strip() != ''):
                        cont.append(res.groups()[0]);
                    file = res.groups()[1];
            if(pat == r'(- .*\n)([\s\S]*)'):
                while(True):
                    res = re.match(pat, file);
                    if(res == None):
                        res = re.match(r'([\t ]+- [\s\S]*?\n)([^\t ]+[\s\S]*)', file);
                        if(res == None):
                            break;
                        if(res.groups()[0].strip() != ''):
                            cont.append(res.groups()[0]);
                        file = res.groups()[1];
                        continue;
                    if(res.groups()[0].strip() != ''):
                        cont.append(res.groups()[0]);
                    file = res.groups()[1];
            if(pat == r'(^>.*?\n)([\s\S]*)'):
                while(True):
                    #print(file);
                    #print('eof\n\n\n\n')
                    res = re.match(pat, file);
                    if(res == None):
                        break;
                    if(res.groups()[0].strip() != ''):
                        cont.append(res.groups()[0]);
                    file = res.groups()[1];
            if(pat == r'([0-9]+[.] [\s\S]*?\n)([\s\S]*)'):
                while(True):
                    res = re.match(pat, file);
                    if(res == None):
                        res = re.match(r'([\t ]+[0-9]+[.] [\s\S]*?\n)([^\t ]+[\s\S]*)', file);
                        if(res == None):
                            break;
                        if(res.groups()[0].strip() != ''):
                            cont.append(res.groups()[0]);
                        file = res.groups()[1];
                        print(cont);
                        continue;
                    if(res.groups()[0].strip() != ''):
                        cont.append(res.groups()[0]);
                    file = res.groups()[1];
            if(len(cont) == 0):
                continue;
            node = element();
            if(pat == r'(\|.*?\n)([\s\S]*)'):
                node.ele_type = 'table';
            elif(pat == r'(^>.*?\n)([\s\S]*)'):
                node.ele_type = 'bq';
            elif(pat == r'(```[\s\S]*?```)([\s\S]*)'):
                node.ele_type = 'cb';
            elif(pat == r'(- .*\n)([\s\S]*)'):
                node.ele_type = 'ul'
            elif(pat == r'(.*\n?)([\s\S]*)'):
                node.ele_type = 'p';
            elif(pat == r'([0-9]+[.] [\s\S]*?\n)([\s\S]*)'):
                node.ele_type = 'ol';
            node.content = cont;
            tree.append(node);
            break;
    return tree;
'''
In the list "tree", there are
elements with property 'ele_type' and 'content'
ele_type:
- 'cb' means code block
- 'ul' means unordered list
- 'p' means plain paragraph
- 'ol' means ordered list
and inside list content, there are
- a simple string, if ele_type == 'p' or 'cb'
- a list of elements in the list, if ele_type == 'ul' or 'ol'
'''

def codesub(i):
    '''
    just c/c++ parser here
    '''
    code = i.content[0].replace('```', '');
    code = code.replace('<', '&lt;');
    code = code.replace('>', '&gt;');
    codetree = [];
    while(True):
        res = re.match(r'([\s\S]*)([/][*][\s\S]*?[*][/])([\s\S]*)', code);
        if(res != None):
            codebr = codeline();
            codebr.code = res.groups()[0];
            codebr.code_type = 'plain';
            if(codebr.code.strip() != ''):
                codetree.append(codebr);
            #print(codebr.code, codebr.code_type);
            #print(codetree);
            codebr0 = codeline();
            codebr0.code = res.groups()[1];
            codebr0.code_type = 'comment';
            if(codebr0.code.strip() != ''):
                codetree.append(codebr0);
            code = res.groups()[2];
        else:
            codebr = codeline();
            codebr.code = code;
            codebr.code_type = 'plain';
            if(codebr.code.strip() != ''):
                codetree.append(codebr);
            break;
    codelist = [];                    
    '''for i in codetree:
        print(i.code);
    print('end\n\n\n\n');'''
    for branch in codetree:
        #print(branch.code, branch.code_type);
        for j in branch.code.split('\n'):
            if(j != ''):
                '''
                if(branch.code_type == 'comment'):
                    codelist.append('<inline class="md-code-comment">' + j + '</inline>');
                else:'''
                #这里应该压入（内容，种类（comment））的对，挖个坑，以后补
                codelist.append(j);
        #print(branch.code, branch.code_type);
    return codelist;

def subkw(cont):
    return cont.groups()[0] + '<span class="code-keyword">' + cont.groups()[1] + '</span>' + cont.groups()[2];

def subbi(cont):
    return '<inline class="md-bi">' + cont.groups()[0] + '</inline>'
def subb(cont):
    return '<inline class="md-b">' + cont.groups()[0] + '</inline>';
def subi(cont):
    return '<inline class="md-i">' + cont.groups()[0] + '</inline>';
def subinlinecode(cont):
    return '<inline class="md-inlinecode">' + cont.groups()[0] + '</inline>';
def subhref(cont):
    #print(cont.groups())
    return '<a class="md-href" href="' + cont.groups()[1] + '">' + cont.groups()[0] + '</a>';
def subpic(cont):
    #print(cont.groups())
    return '<img class="md-img" src="' + cont.groups()[1] + '" alt="' + cont.groups()[0] + '">';

def subinline(cont):
    while(True):
        modified = False;
        for i in range(0, len(inlinepat)):
            res = re.search(inlinepat[i], cont);
            if(res != None):
                cont = re.sub(inlinepat[i], inlinefunc[i], cont);
                modified = True;
                break;
        if(modified == False):
            break;
    return cont;
'''
这里又有一个bug：
行内代码处理完之后，里面的内容不应该再进行其他行内渲染，而应该直接遵从代码渲染
公式同理，所以两者应该一起搞
'''
def decorate(tree, finhtml):
    #print(finhtml);
    #print('1\n\n');
    for i in tree:
        if(i.ele_type == 'p'):
            modified = False;
            for j in range(0, 6):
                #print(i.content[0].strip());
                res = re.match(hpat[j], i.content[0].strip());
                #print(res);
                if(res != None):
                    i.ele_type = 'h' + str(6-j);
                    i.content = '<' + i.ele_type + ' class="md-' + i.ele_type + '">' + res.groups()[0].replace(' ', '&nbsp;') + '</' + i.ele_type + '>';
                    modified = True;
                    break;
            if(modified == False):
                cont = subinline(i.content[0].strip().replace(' ', '&nbsp;'));
                i.content = '<' + i.ele_type + ' class="md-' + i.ele_type + '">' + cont + '</' + i.ele_type + '>';
            finhtml += i.content;
        elif(i.ele_type == 'cb'):
            finhtml += ('<div class="c-codeblock">');
            codelist = codesub(i);
            for codepiece in codelist:
                codepiece = codepiece.replace('\t', '    ');
                codepiece = codepiece.replace(' ', '&nbsp;');
                for i in range(0, len(keyword)):
                    #print(re.sub('('+keyword[i]+')', subkw, codelist[j]))
                    codepiece = re.sub('([^a-zA-Z]?)('+keyword[i]+')([^a-zA-Z]?)', subkw, codepiece);
                finhtml += codepiece;
                finhtml += '<br/>';
            finhtml += '</div>';
        elif(i.ele_type == 'bq'):
            finhtml += '<blockquote class="md-quote">'
            bqls = i.content;
            #print(bqls);
            newfile = '';
            for bqcont in bqls:
                s = bqcont.replace('>', '',1);
                newfile += s.lstrip();
            #print(newfile);
            ntree = buildtree(newfile);
            finhtml = decorate(ntree, finhtml);
            finhtml += '</blockquote>';
        elif(i.ele_type == 'ul'):
            cont = ''
            for j in i.content:
                cont += j;
            finhtml += decul(cont);
        elif(i.ele_type == 'ol'):
            cont= ''
            for j in i.content:
                cont += j;
            #print(cont);
            #print('1\n\n');
            finhtml += decol(cont);
        elif(i.ele_type == 'table'):
            cont = '';
            for j in i.content:
                cont += j;
            finhtml += dectable(cont);
    return finhtml;

def decul(cont):
    ret = '<ul class="md-ul-li">';
    lis = cont.split('\n');
    i = 0;
    while(i < len(lis)):
        if(lis[i].strip() == ''):
            i += 1;
            continue;
        res = re.match(r'  - (.*)', lis[i]);
        cont0 = '';
        while(res != None):
            cont0 += (res.groups()[0] + '\n');
            i += 1;
            res = re.match(r'  - (.*)', lis[i]);
        if(cont0 != ''):
            ret += decul(cont0);
        if(res != None):
            ret += decul(res.groups()[0]);
        else:
            ret += '<li class="md-ul-li">' + subinline(lis[i].replace('- ', '', 1).replace(' ', '&nbsp;')) + '</li>';
        i += 1;
    return ret + '</ul>';

def decol(cont):
    ret = '<ol class="md-ol">';
    #print(cont);
    lis = cont.split('\n');
    i = 0;
    while(i < len(lis)):
        if(lis[i].strip() == ''):
            i += 1;
            continue;
        res = re.match(r'[ ]{3,4}([0-9]+[.].*)', lis[i]);
        cont0 = '';
        while(res != None):
            cont0 += (res.groups()[0] + '\n');
            #print(res.groups()[0]);
            i += 1;
            res = re.match(r'[ ]{3,4}([0-9]+[.].*)', lis[i]);
        if(cont0 != ''):
            s = decol(cont0);
            print(s);
            ret += s;
        if(i < len(lis) and lis[i].strip() != ''):
            ret += '<li class="md-ol-li">' + subinline(re.sub('([0-9]+[.][ ])', '', lis[i], 1).replace(' ', '&nbsp;')) + '</li>';
        i += 1;
    return ret + '</ol>';

def dectable(cont):
    ret = '<table class="md-table"><tbody class="md-tbody">';
    lis = cont.split('\n');
    #print('lis:',lis);
    isth = True;
    havcont = False;
    for tr in lis:
        cur = tr;
        havcont = False;
        listd = tr.split('|');
        #print(listd);
        isline = False;
        for i in range(0, len(listd)):
            #print(td);
            #print(re.match(r'[\-]+', td.strip()) != None);
            if(listd[i].strip() != '' and re.match(r'[\-]+', listd[i].strip()) == None):
               break;
            #print(td);
            if(i == len(listd)-1):
               isth = False;
               isline = True;
        if(isline):
            continue;
        for td in listd:
            if(td.strip() == ''):
                continue;
            if(havcont == False):
                ret += '<tr class="md-tr">';
                havcont = True;
            #print(td);
            if(isth):
                ret += '<th class="md-th">' + td + '</th>';
            else:
                ret += '<td class="md-td">' + td + '</td>';
        if(havcont):
            ret += '</tr>'
    return ret + '</tbody></table>';

class element:
    ele_type = 'para';
    content = [];

class codeline:
    code = '';
    code_type = '';

pattern = [r'(^>.*?\n)([\s\S]*)', r'(```[\s\S]*?```)([\s\S]*)', r'(\|.*?\n)([\s\S]*)', r'(- .*\n)([\s\S]*)', r'([0-9]+[.] [\s\S]*?\n)([\s\S]*)',r'(.*\n?)([\s\S]*)']
hpat = [r'###### (.*)', r'##### (.*)', r'#### (.*)', r'### (.*)', r'## (.*)', r'# (.*)'];
keyword = ['char', 'short', 'int', 'long', 'long long', 'float', 'double',
           'return', 'for', 'if', 'while', 'do', 'auto'];
#cnt=0;
inlinepat = [r'\*\*\*(.*?)\*\*\*' ,r'\*\*(.*?)\*\*', r'[*](.*?)[*]', r'`(.*?)`', r'!\[(.*?)\]\((.*?)\)', r'\[(.*?)\]\((.*?)\)'];
inlinefunc = [subbi, subb, subi, subinlinecode, subpic, subhref];


file = '';
with open(filename + '.md', 'rt', encoding='utf-8') as f:
    file = f.read();
file = file + '\n';
fhtml = '''
<html>
<head>
<link rel="stylesheet" type="text/css" href="./style.css" />
</head>
<body>
''';
tr = buildtree(file);
fhtml = decorate(tr, fhtml);
with open(filename + '.html', 'wt', encoding="utf-8") as f:
    f.write(fhtml + '''<script type="text/javascript"
src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML">
</script>
<script type="text/x-mathjax-config">
MathJax.Hub.Config({
tex2jax: {inlineMath: [['$','$']]}
});
</script></body></html>''');
#print(fhtml);
'''
<script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
<script type="text/x-mathjax-config">
MathJax.Hub.Config({
tex2jax: {inlineMath: [['$','$'], ['\(','\)']]}
});
</script>'''
