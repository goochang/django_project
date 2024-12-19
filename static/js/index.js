$(document).ready(function() {
    // 이미지 미리보기
    $("div.user_photo_wrap input#id_photo").change(function(event) {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();

            reader.onload = function(e) {
                $("img#user_photo").attr("src", e.target.result).show();
            };

            reader.readAsDataURL(file);
        }
    });

    // 이미지 미리보기
    $("div.productEditWrap input#id_photo").change(function(event) {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();

            reader.onload = function(e) {
                $(".productEditWrap .imgWrap img").attr("src", e.target.result).show();
            };

            reader.readAsDataURL(file);
        }
    });

    // 이미지 영역 클릭시 input file 활성화
    $("img#user_photo").click(function(event){
        $("input#id_photo").click();
    })

    // 자기소개 입력 길이 제한
    oldVal = ""
    if($("input[name='introduce']").length){
        $("p.limit-intro-num").text($("input[name='introduce']").val().length + "/20")
    }
    $("input[name='introduce']").on("change keyup paste", function() {
        var currentVal = $(this).val();
        if(currentVal == oldVal || currentVal.length > 20) {
            $(this).val(oldVal)
            return;
        }

        $("p.limit-intro-num").text(currentVal.length + "/20")
     
        oldVal = currentVal;
        console.log(currentVal.length);
    });
    
});
