function favor(obj) {
    var favor = obj.getAttribute("data-favor");
    var id = obj.getAttribute("data-id");
    var date  = obj.getAttribute("data-date");
    if (obj.getAttribute("data-select") == "true") {
        obj.className = "btn btn-default";
        obj.setAttribute("data-select", "false");
        var newFavor = parseInt(favor) - 1;
        localStorage[id+date] = "false";
    } else {
        obj.className = "btn btn-primary";
        obj.setAttribute("data-select", "true");
        var newFavor = parseInt(favor) + 1;
        localStorage[id+date] = "true";
    }
    showFavor(obj, newFavor);
    obj.setAttribute("data-favor", newFavor);
    $.post(
        "/main/favor/",
        {
            "id": id,
            "date": date,
            "favor": localStorage[id+date],
        },
        function (data) {
        },
        "json"
    );
}

function initFavor() {
    var obj = document.getElementById("favor");
    if (obj == null) {
        return;
    }
    var favor = obj.getAttribute("data-favor");
    var id = obj.getAttribute("data-id");
    var date  = obj.getAttribute("data-date");
    if (localStorage[id+date] == "true") {
        obj.className = "btn btn-primary";
        obj.setAttribute("data-select", "true");
    } else if (localStorage[id+date] == "false"){
        obj.className = "btn btn-default";
        obj.setAttribute("data-select", "false");
    }
    showFavor(obj, favor);
}

function showFavor(obj, newFavor) {
    if (newFavor > 0) {
        obj.innerHTML = "<span class=\"glyphicon glyphicon-thumbs-up\"></span> 赞("+newFavor+")";
    } else if (newFavor === 0) {
        obj.innerHTML = "<span class=\"glyphicon glyphicon-thumbs-up\"></span> 赞";
    }
}

function deleteBlog(blog_id) {
    $.post(
        "/delete-blog/" + blog_id + "/",
        function (data) {
            if (data.status == "suc") {
                window.location.href = "/main/";
            } else {
                alert("删除失败");
            }
        },
        "json"
    );
}

function login() {
    $.post(
        "/main/login/",
        {
            username: $("#username").val(),
            password: $("#password").val(),
        },
        function (data) {
            var btn = $("#login-button");
            var btnText = btn.html();
            if (data.status == "suc") {
                btn.html(btnText.replace(/登录/, "登出").replace(/glyphicon glyphicon-user/, "glyphicon glyphicon-remove"))
                btn.attr("onclick", "logout()");
                btn.attr("data-toggle", "");
                $("#write-blog").html("<a href='/write/'><span class='glyphicon glyphicon-pencil'></span> 写博客</a>");
                $("#login-dialog").modal('hide');
            } else {
                $("#login-button").html(btn.html().replace(/登出/, "登录").replace(/glyphicon glyphicon-remove/, "glyphicon glyphicon-user"))
                $("#request-text").html("登录失败");
            }
        },
        "json"
    );
}

function logout() {
    $.post("/main/logout/", {}, function (data) {
        if (data.status == "suc") {
            //$("#write-blog").html("");
            //$("#login-button").attr("onclick", "login()");
            //$("#login-button").attr("data-toggle", "modal");
            location.reload();
        }
    }, "json");
    return false;
}

// 监听窗口的滚动来显示返回最顶端按钮
function addScrollListener() {
    var upBtnIsShow = false;
    var showUpBtnHeight = $(window).height() / 3;
    $(window).scroll(function (event) {
        if ($(this).scrollTop() > showUpBtnHeight && !upBtnIsShow){
            upBtnIsShow = true;
            $("#scroll-up").fadeIn();
            return;
        }
        if ($(this).scrollTop() < showUpBtnHeight && upBtnIsShow){
            upBtnIsShow = false;
            $("#scroll-up").fadeOut();
            return;
        }
    });
}

function initLayout() {
    initFavor();
    addScrollListener();
}

window.onload = initLayout();