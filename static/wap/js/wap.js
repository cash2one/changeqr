var oWap ={
	operator:function(){
		//一些小操作
		$(".video_show").unbind("click");
		//关闭广告
		$(".ad_close_btn").on("click",function(){
			$(".footer").hide();
			var code = $(".code").val();
			//$.post("/api/close_ad",{
			//	code:code
			//}, function(){});
            //使用原生js写这个post请求，避免jquery冲突
            var xmlhttp = new XMLHttpRequest();
            xmlhttp.open("POST", "/api/close_ad", true);
            xmlhttp.setRequestHeader("Content-type","application/x-www-form-urlencoded");
            var queryStr = "code=" + code
            xmlhttp.send(queryStr);
		});
	},
	video_play:function(){
		//视频播放
		$(".vedio_play").on("click",".play,#videoTap",function(e){
			e.stopPropagation();
			var $this = $("#videoTap")[0];
			$this.play();
			$this.webkitEnterFullscreen();
		})
	},
	init:function(){
		this.operator();
		this.video_play();
	}
}

$(function(){
	oWap.init();
});

