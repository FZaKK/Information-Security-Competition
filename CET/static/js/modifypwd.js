$(function(){
    var error_password = false ;
    var error_check_password =false;

    $('#new_password1').blur(function(){
        check_pwd();

    });
    $('#new_password2').blur(function(){
        check_cpwd();

    });

    function check_pwd(){
        var len = $('#new_password1').val().length;
//        if (len<8 || len>20){
//        $('#new_password1').next().html('密码最少8位，最长20位')
//        $('#new_password1').next().show();
//        error_password=true;
//
//        }
//        else{
        $('#new_password1').next().hide();
        error_password = false;
        }



    function check_cpwd(){
        var pass = $('#new_password1').val();
        var cpass = $('#cpwd').val();
        if(pass!=cpass){
        $('#new_password2').next().html('两次输入的密码不一致')
        $('#new_password2').next().show();
        error_check_password=true;

    }
    else{
        $('#new_password1').next().hide();
        error_check_password=true;

    }


    }

    $('#modify_form').submit(function(){
        check_pwd();
        check_cpwd();

        if(error_password == false && error_check_password == false){
        return true;
        }
        else{
        return false;
        }
    })


    });



});