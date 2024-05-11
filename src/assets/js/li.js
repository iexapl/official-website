// JavaScript Document
// author:hang li;
//date:2013/10/18


//多选项卡切换
//多选项卡切换, zhang added ,修改了, 加了index
function T_qiehuan(choice,cssS,callback,index){
 	if(!index){
 		index = 0;
 	}
	//把所有目标选项隐藏
	function HiddenAim(){
		$(choice).each(function() {
			$("#"+$(this).attr("aim")).hide();
		});
	}
	$(choice).hover(function(){
		if($(this).attr("aim")){//判断是否有aim属性，有此属性才执行
			currentId=$(this).attr("aim");
			HiddenAim();
			$("#"+currentId).show();//显示目标选项
			$(this).addClass(cssS).siblings().removeClass(cssS);//移除当前选中的样式
			//回调函数
			if(callback)
			{
				var index=$(this).index();
				callback.call(this,index);
			}
		}
	})//初始化事件
		//把所有目标隐藏
		.each(function(){
			$("#"+$(this).attr("aim")).hide();
		})
		//为初始化默认值添加样式和显示目标选项
		.eq(index).addClass(cssS);
	var firstDisId=$(choice).eq(index).attr("aim");
	$("#"+firstDisId).show();
};

//滚动方法
//五个参数，一个必选参数，对象，方向，速度，左键ID，右键ID
function picscroll(obj,way,speed,leftBtnId,rightBtnId)
{
	this.init.call(this,obj,way,speed,leftBtnId,rightBtnId)
}
picscroll.prototype={
	init:function(obj,way,speed,leftBtnId,rightBtnId)
	{
		var _this=this;
		this.obj=$(obj);
		this.obj.css("overflow","hidden");
		this.ul=this.obj.find("ul");//ul对象
		this.li=this.ul.children("li");//li对象
		this.objW=parseInt(this.obj.css("width"));//可视区域的长宽，必须CSS里设置，否则IE读取不出宽度！！！
		this.objH=parseInt(this.obj.css("height"));
		this.maxW=0;
		this.maxH=0;
		for(var i=0;i<this.li.length;i++)
		{
			this.maxW+=this.li.eq(i).outerWidth(true);//滚动最大宽度,分别计算每个LI的宽度
		}
		for(var i=0;i<this.li.length;i++)
		{
			this.maxH+=this.li.eq(i).outerHeight(true);//可滚动最大高度,分别计算每个LI的高度
		}
		this.way=way || 1;//滚动方向
		this.speed=speed?speed:50;
		if(leftBtnId)
		{
			this.lBtn=$("#"+leftBtnId);
			this.lBtn.click(function(){
				_this.way=4;
			})
		}
		if(rightBtnId)
		{
			this.rBtn=$("#"+rightBtnId);
			this.rBtn.click(function(){
				_this.way=2;
			})
		}
		if(this.way==1)//条件判断是否滚动
		{
			if(this.objH<this.maxH)this.is();
		}else if(this.way==2||this.way==4)
		{
			if(this.objW<this.maxW)this.is();
		}

	},
	is:function(){
		var _this=this;
		this.ul.append(this.ul.html());//ul里内容加倍
		this.lili=this.ul.children("li");//加倍后的li;
		if(this.way==2||this.way==4)this.ul.css("width",2*this.maxW);//为UL增加宽度
		this.int=0;//用于记录滚动值，初始为0;
		this.gogo();
		this.lili.hover(function(){
			_this.rest();
		},function(){
			_this.gogo();
		});
	},
	run:function()
	{
		switch(this.way)
		{
			case 1:
				if(this.int>=this.maxH)
				{
					this.int=0;
					this.obj.scrollLeft(0);
				}
				this.int+=2;
				this.obj.scrollTop(this.int);
				break;
			case 2:
				if(this.int==0)
				{
					this.int=this.maxW;
					this.obj.scrollLeft(this.int);
				}
				this.int-=2;
				this.obj.scrollLeft(this.int);
				break;
			case 4:
				if(this.int>=this.maxW)
				{
					this.int=0;
					this.obj.scrollLeft(0);
				}
				this.int+=2;
				this.obj.scrollLeft(this.int);
				break;
		}
	},
	gogo:function()
	{
		var _this=this;
		this.timer=setInterval(function(){_this.run();},this.speed);
	},
	rest:function()
	{
		clearInterval(this.timer);
	}
}

