MM_CRAWLER

实现思路
1.图片URL的提取
首先是对www.22mm.cc主页的分析。在主页上的图片都是小图，当然不能要，但是有进入的链接，其源代码如：
href="/mm/bagua/PiaHdPdeabPaHidPa.html"

格式为/mm/*/第一个为大写字母.html
所以在用getHtml函数获取到的html源代码中使用正则表达式 /mm/[a-z]+/[A-Z][A-Za-z]+.html 可以提取出来，然后再前面拼上"http://www.22mm.cc"就组成了大图页面的URL，大图页面的URL就是我们需要的。
再来分析大图页面的源代码，在分析过程中发现每组图的最后一个页面的源代码中有整组图的URL，如下：
var arrayImg=new Array();
arrayImg[0]="http://bgimg1.meimei22.com/big/bagua/2014-3-21/1/6369576220140225100634074_640.jpg";
arrayImg[0]="http://bgimg1.meimei22.com/big/bagua/2014-3-21/1/6369576220140225100657062_640.jpg";
arrayImg[0]="http://bgimg1.meimei22.com/big/bagua/2014-3-21/1/6369576220140225100714069_640.jpg";
arrayImg[0]="http://bgimg1.meimei22.com/big/bagua/2014-3-21/1/6369576220140225100728045_640.jpg";
arrayImg[0]="http://bgimg1.meimei22.com/big/bagua/2014-3-21/1/6369576220140225100742039_640.jpg";
arrayImg[0]="http://bgimg1.meimei22.com/big/bagua/2014-3-21/1/6369576220140225100757026_640.jpg";
arrayImg[0]="http://bgimg1.meimei22.com/big/bagua/2014-3-21/1/6369576220140225100812026_640.jpg";
arrayImg[0]="http://bgimg1.meimei22.com/big/bagua/2014-3-21/1/6369576220140225100827083_640.jpg";
arrayImg[0]="http://bgimg1.meimei22.com/big/bagua/2014-3-21/1/6369576220140225100842068_640.jpg";
arrayImg[0]="http://bgimg1.meimei22.com/big/bagua/2014-3-21/1/6369576220140225100856064_640.jpg";
arrayImg[0]="http://bgimg1.meimei22.com/big/bagua/2014-3-21/1/6369576220140225100912068_640.jpg";
arrayImg[0]="http://bgimg1.meimei22.com/big/bagua/2014-3-21/1/6369576220140225100928069_640.jpg";
arrayImg[0]="http://bgimg1.meimei22.com/big/bagua/2014-3-21/1/6369576220140225100940014_640.jpg";
getImgString()

所以只用保存每组图的最后一个页面的URL就行了。其中最后一个页面的URL是形如：www.22mm.cc/mm/bagua/PiaHdPdeabPaHidPa-13.html，而从主页上进来的链接为：www.22mm.cc/mm/bagua/PiaHdPdeabPaHidPa.html，所以只用找到每组图片的张数再跟源链接进行拼接就行了。而在网页上有整组图片的张数，所以找到对应的源代码为形如：
<strong class="diblcok"><span class="fColor">13</span>/13</strong>

所以在正则表达式中</span>/\d+</strong> 然后用replace去掉</span>/和</strong>标签就能提取出来张数。
然后把张数跟开始得到的大图页面URL拼接成 "http://www.22mm.cc/mm/bagua/PiaHdPdeabPaHidPa-13.html"的格式。
到此为止就得到了大图页面的URL列表，存储在htmlList里面。

然后把htmlList传给getImgList函数，在该函数中通过getHtml获得大图页面的源代码，再使用正则表达式 0]="http://\S*?.jpg 并replace掉"0]="之后便获得整组大图图片的URL，并存放在imgList里。

但是通过后面运行发现是有问题的，通过chrome的审查元素发现真实的图片URL为:
http://bgimg1.meimei22.com/pic/bagua/2014-3-21/1/6369576220140225100940014_640.jpg

为不是通过源代码获得的:
http://bgimg1.meimei22.com/big/bagua/2014-3-21/1/6369576220140225100940014_640.jpg

原因可能是因为图片是用js加载上去的，不是在源代码里写明确的。
于是通过一个replace把big替换成pic就行了。
至此URL提取已经完成。

2.图片的下载

通过传递的参数可以设定爬取图片的数量，就把刚得到的URL列表通过循环把设定数量的URL加入到多线程下载过程中要使用的队列里面。
再根据设定的线程数量通过循环建立几个线程，并把URL队列及设定的存储位置当参数传入线程类。
在线程类的构造函数对传入参数进行初始化，然后对run函数进行重载。然后从URL队列里出队一个URL，使用urllib.request.urlretrieve下载对应图片，下载中使用try，要是出现网络等问题图片没有下载成功时，抛出一个异常打印出来并把该URL入队。当URL队列为空时，即图片下载完成。


