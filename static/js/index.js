$(document).ready(function() {
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
    $("img#user_photo").click(function(event){
        $("input#id_photo").click();
    })

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

    var poke_id, weight, height = 0;
    // 포켓몬 불러오기
    if($("input[name='poke_eng_name']").length){
        
        var poke_name = $("input[name='poke_eng_name']").val()
        
        $.ajax({
            url: "https://pokeapi.co/api/v2/pokemon/" + poke_name,
            method: 'GET',
            beforeSend: function() {
                $("div.loading").addClass("active");
            },
            success: function(data) {
                poke_id = data["id"];
                weight = data["weight"];
                height = data["height"];
                abilities = data["abilities"];
                console.log(data)

                // 포켓몬 설명 불러오기
                var types = data["types"].map((type) => type.type.name);
                if(types.length > 0){
                    $(".detailMainWrap .info_wrap").addClass(types[0])
                    for (let i = 0; i < types.length; i++) {
                        $(".info_wrap .poke_types .type" + (i+1)).addClass(types[i])
                        $(".info_wrap .poke_types .type" + (i+1) + " img").attr("src", "/static/icons/" + types[i] + ".svg")
                        $(".info_wrap .poke_types .type" + (i+1)).css("display", "block")
                    }
                }

                if(poke_id != ""){
                    poke_flavor(poke_id)
                }

                // 포켓몬 특성 불러오기
                for (let i = 0; i <= abilities.length; i++) {
                    var ability_url = abilities[i]["ability"]["url"];

                    if(ability_url !== ""){
                        get_ability(ability_url, i);
                        if(i = abilities.length){
                            $("div.card_abilities").css("display", "block")
                        }
                    }
                }
            },
            error: function(jqXHR, textStatus, errorThrown) {
                console.log('요청 실패:', textStatus, errorThrown);
                alert('오류가 발생했습니다: ' + textStatus);
            },
            complete: function() {
                setTimeout(() => {
                    $("div.loading").removeClass("active");                    
                }, 1000);
            }
        });
    }
    // 포켓몬 설명 불러오기
    function poke_flavor(poke_id){
        $.ajax({
            url: "https://pokeapi.co/api/v2/pokemon-species/" + poke_id,
            method: 'GET',
            success: function(data){
                console.log(data)
                if(data.flavor_text_entries){
                    var flavor_text = data.flavor_text_entries.filter((info) => info.language.name == "ko")
                    if( flavor_text.length ){
                        flavor_text = flavor_text[flavor_text.length-1].flavor_text
                    }
                    var genera = data.genera.filter((info) => info.language.name == "ko")
                    if( genera.length ){
                        genera = genera[genera.length-1].genus
                    }
                    $("div.card_flavor span.flavor").text(flavor_text);
                    $("div.card_flavor span.weight").text("몸무게 : " + Math.round(weight * 100) / 1000 + "kg");
                    $("div.card_flavor span.height").text("키 : " + Math.round(height * 100) / 1000 + "m");
                    $("div.card_flavor span.genera").text(genera);
                }
            }
        });
    }
    // 포켓몬 특성 불러오기
    function get_ability(_url, i){
        $.ajax({
            url: _url,
            method: 'GET',
            success: function(data){
                if(data.flavor_text_entries){
                    var flavor_text = data.flavor_text_entries.filter((info) => info.language.name == "ko")
                    if( flavor_text.length ){
                        flavor_text = flavor_text[flavor_text.length-1].flavor_text
                    }
                    var name = data.names.filter((info) => info.language.name == "ko")
                    if( name.length ){
                        name = name[name.length-1].name
                    }
                    
                    $("div.card_abilities .ability"+ i + " b").text(name)
                    $("div.card_abilities .ability"+ i + " span").text(flavor_text)
                    $("div.card_abilities .ability"+ i).css("display", "block")
                }
            }
        });
    }

    var product_id = $("input[name='product_id']").val();

    $("button.followBtn").click(function(){
        var csrftoken = $("[name=csrfmiddlewaretoken]").val();
        $.ajax({
            url: "/account/follow/",
            headers:{
                "X-CSRFToken": csrftoken
            },
            data: {
                "product_id" : product_id,
            },
            method: 'POST',
            success: function(data){
                console.log(data)
                if(data.follow.isActive){
                    $("button.followBtn").text("팔로잉")
                } else{
                    $("button.followBtn").text("팔로우")
                }
            }
        })
    });
                
    $("button.wishBtn").click(function(){
        var csrftoken = $("[name=csrfmiddlewaretoken]").val();
        $.ajax({
            url: "/product/wish/",
            headers:{
                "X-CSRFToken": csrftoken
            },
            data: {
                "product_id" : product_id,
            },
            method: 'POST',
            success: function(data){
                console.log(data)
                $("button[name='wishBtn'] span").text(data.wishCnt)
                if(data.wish.isActive){
                    $("button[name='wishBtn']").addClass("active")
                } else {
                    $("button[name='wishBtn']").removeClass("active")
                }
            }
        });

    });
    
});
