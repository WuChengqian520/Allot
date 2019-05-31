function Index(){
    this.submitBtn = $("#submit");
    this.inputName = $("input[name='name']");
    this.line = $(".line");
    this.deleteBtn = $(".delete");

    var csrf=$("input[name='csrfmiddlewaretoken']").attr("value");
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrf)
        }
    });
}

Index.prototype.listenSubmitEvent = function(){
    var self = this;
    this.submitBtn.click(function () {
        var name = self.inputName.val();
        $.post({
            url: '/addName/',
            data:{
                name: name
            },
            success: function (result) {
                if (result['code'] === 200){
                    alert("添加成功！");
                    window.location.reload()
                }else{
                    alert(result['msg'])
                }
            },
            fail: function (error) {
                alert(error)
            }
        });
    });
};

Index.prototype.listenHoverEvent = function(){
    var slef = this;
    slef.line.hover(function (event) {
        var deleteBtn = $(this).find('.delete');
        deleteBtn.show();
    }, function () {
        var deleteBtn = $(this).find('.delete');
        deleteBtn.hide();
    });
};

Index.prototype.listenRemoveEvent = function(){
    var self = this;
    self.deleteBtn.click(function () {
        var id = $(this).parent().parent().attr('name-id');
        $.post({
           url: '/remove/',
           data: {
               id: id
           },
            success: function (result) {
                if (result['code'] === 200){
                    alert("删除成功");
                    window.location.reload();
                }else{
                    alert("删除失败")
                }
            }
        });
    });
};

Index.prototype.run = function(){
    this.listenSubmitEvent();
    this.listenHoverEvent();
    this.listenRemoveEvent();
};

$(function () {
    var index = new Index();
    index.run();
});
