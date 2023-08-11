// 点击按钮发送验证码
$(document).ready(function() {
$('#btn_send').click(function(){
    //文本框获取手机号码
    var phone = $('#account').val();
    console.log("手机号码：" + phone);
    //可以添加手机号码保证为11位的
    //通过ajax发送请求
    $.getJSON('/user/send',{phone:phone},function(data){
        alert(data.msg);

    });
});
});