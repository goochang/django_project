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
    // 이미지 영역 클릭시 input file 활성화
    $("div.productEditWrap div.imgWrap").click(function(event){
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

    var profile_id = $("input[name='profile_id']").val();
    var csrftoken = $("[name=csrfmiddlewaretoken]").val();

    $("button.followBtn").click(function(){
        $.ajax({
            url: "/account/follow/",
            headers:{
                "X-CSRFToken": csrftoken
            },
            data: {
                "profile_id" : profile_id,
            },
            method: 'POST',
            success: function(data){
                console.log(data)
                if(data.follow.isActive){
                    $("button.followBtn").text("팔로잉")
                } else{
                    $("button.followBtn").text("팔로우")
                }

                $(".user_info .menu .following").text("팔로잉 : " + data.followCnt)
            }
        })
    });

    $("div.btn_wrap button.sort_btn").click(function(e){
        sort = $(e.target).val()
        // 현재 URL에서 기존 쿼리 파라미터를 가져옵니다.
        const urlParams = new URLSearchParams(window.location.search);

        // 'query' 파라미터는 이미 URL에 존재하므로 'sort'만 추가합니다.
        urlParams.set('sort', sort);

        // 새 URL로 페이지 이동
        window.location.search = urlParams.toString();
        // location.href = "?sort="+sort

    })
    
});
