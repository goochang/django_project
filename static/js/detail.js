// 포켓몬 불러오기
function poke_loading(){
    var poke_name = $("input[name='poke_eng_name']").val()
    if(poke_name !== ""){
        $.ajax({
            url: "https://pokeapi.co/api/v2/pokemon/" + poke_name,
            method: 'GET',
            beforeSend: function() {
                $("div.loading").addClass("active");
            },
            success: function(data) {
                console.log(data)
                var poke_id = data["id"];
                var weight = data["weight"];
                var height = data["height"];
                var abilities = data["abilities"];

                $("div.card_flavor span.weight").text("몸무게 : " + Math.round(weight * 100) / 1000 + "kg");
                $("div.card_flavor span.height").text("키 : " + Math.round(height * 100) / 1000 + "m");
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
                    poke_flavor(poke_id);
                }

                if(abilities.length > 0){
                    fetchAbilities(abilities);
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
                $("div.card_flavor span.flavor").text(flavor_text);
            }
            if(data.genera){
                var genera = data.genera.filter((info) => info.language.name == "ko")
                if( genera.length ){
                    genera = genera[genera.length-1].genus
                }
                $("div.card_flavor span.genera").text(genera);
            }
        }
    });
}

async function fetchAbilities(abilities) {
    // 모든 비동기 요청을 처리하는 배열
    let promises = [];

    for (let i = 0; i < abilities.length; i++) {
        const ability_url = abilities[i]["ability"]["url"];
        console.log(abilities[i]["ability"]["name"]);

        if (ability_url !== "") {
            // 각 비동기 요청을 배열에 추가
            promises.push(get_ability(ability_url, i));
        }
    }

    // 모든 비동기 요청이 완료되면 이후 코드 실행
    await Promise.all(promises);
    $("div.card_abilities").css("display", "block");
}

// 포켓몬 특성 불러오기
function get_ability(_url, i){
    return $.ajax({
        url: _url,
        method: 'GET',
        success: function(data){
            console.log(data)
            if(data.flavor_text_entries){
                var flavor_text = data.flavor_text_entries.filter((info) => info.language.name == "ko")
                if( flavor_text.length ){
                    flavor_text = flavor_text[flavor_text.length-1].flavor_text
                }
                var name = data.names.filter((info) => info.language.name == "ko")
                if( name.length ){
                    name = name[name.length-1].name
                }
                
                $("div.card_abilities .ability"+ (i+1) + " b").text(name)
                $("div.card_abilities .ability"+ (i+1) + " span").text(flavor_text)
                $("div.card_abilities .ability"+ (i+1)).css("display", "block")
            }
        }
    });
}
$(document).ready(function() {
    var product_id = $("input[name='product_id']").val();
    var csrftoken = $("[name=csrfmiddlewaretoken]").val();
    poke_loading();
                
    $("button.wishBtn").click(function(){
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

    $("div.card_action button.deleBtn").click(function(){
        var result = confirm("정말 삭제하시겠습니까.");
        if(result){
            $.ajax({
                url: "/product/"+product_id+"/delete/",
                headers:{
                    "X-CSRFToken": csrftoken
                },
                method: 'POST',
                success: function(data){
                    console.log(data)
                    location.href = "/"
                },
                error: function(data){
                    console.log(data)

                }
            });
        }
    });

    $("button[name='editBtn']").click(function(e){
        location.href = "/product/"+product_id+"/edit/";
    });
    
});
