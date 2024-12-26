$(document).ready(function() {

    $("div.hashtags_input input").on("keydown", function(e){
        val = $(e.target).val()
        console.log(e.keyCode)
        if(e.keyCode == 32){
            e.preventDefault();
            if(val !== ""){
                val_list = $("div.hashtags_wrap span").map((_, el) => $(el).text()).get()
                console.log(val_list)
                console.log()

                // 해시태그 입력 성공
                if(val_list.length == 0 || val_list.filter( (v) => "#"+val == v ).length == 0){
                    $("div.hashtags_wrap").append("<span>#" + val + "</span>")
                    $(this).val("")
                    $(".input_error").text("")

                    hashtags_input = $("input[name='hashtags']").val()
                    $("input[name='hashtags']").val(hashtags_input+"|"+val)
                } else{ // 해시태그 입력 실패
                    $(".input_error").text("이미 등록된 해시태그입니다.")
                }



            }
        } else if(e.keyCode == 8){
            hashtags_wrap = $("div.hashtags_wrap span")
            if(val == "" && hashtags_wrap.length){
                console.log("삭제")
                $("div.hashtags_wrap span:last-child").remove()

                lindex = $("input[name='hashtags']").val().lastIndexOf('|')
                lval = $("input[name='hashtags']").val().substring(0,lindex)
                $("input[name='hashtags']").val(lval)


            }

        }
    })
    
    
});
