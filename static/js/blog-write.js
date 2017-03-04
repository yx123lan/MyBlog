function saveBlogCache() {
    localStorage.cacheBlogTitle = $("#title").val();
    localStorage.cacheBlogContent = $("#content").val();
    setTimeout(saveBlogCache, 1000 * 8);
}

function readBlogCache() {
    if (localStorage.cacheBlogTitle) {
        $("#title").val(localStorage.cacheBlogTitle);
    }
    if (localStorage.cacheBlogContent) {
        $("#content").val(localStorage.cacheBlogContent);
    }
    setTimeout(saveBlogCache, 1000 * 8);
}

function clearBlogCache() {
    localStorage.cacheBlogTitle = "";
    localStorage.cacheBlogContent = "";
}

function selectTag(obj) {
    $("#tag").val(obj.innerHTML);
    $("#select-tag").html(obj.innerHTML + " <span class='caret'>");
}

function submit(obj) {
    if (obj.id == "save-blog") {
        ajaxSave();
    } else if(obj.id == "submit-blog") {
        ajaxSubmit();
    } else {
        $("#blog").submit();
    }
    if (obj.id == "save-blog" || obj.id == "submit-blog") {
        clearBlogCache();
    } else {
        saveBlogCache();
    }
    return false;
}

function ajaxSave() {
    $.post("/save-blog/", {
            tag: $("#tag").val(),
            title: $("#title").val(),
            content: $("#content").val(),
        },
        function (data) {　　
            if (data.status == "suc") {
                alert("保存成功");　　
            } else {
                alert("保存失败");　　
            }
        },
        "json"
    );
}

function ajaxSubmit() {
    $.post("/submit-blog/", {
            tag: $("#tag").val(),
            title: $("#title").val(),
            content: $("#content").val(),
        },
        function (data) {　　
            if (data.status == "suc") {
                window.location.href = data.url;　　
            }　else {
                alert("提交失败");　　
            }
        },
        "json"
    );
}

function isEmpty(str) {
    if(str == null || typeof str == "undefined" ||
            str == ""){
        return true;
    }
    return false;
}

// 尝试加载浏览器本地缓存
if (isEmpty($("#content").val())) {
    window.onload = readBlogCache();
}