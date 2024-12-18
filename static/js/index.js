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

    if( $("div.detailContainer").length){
        $("div.loading").addClass("active");
    }
    // 포켓몬 불러오기
    if($("input[name='poke_eng_name']").length){

        var poke_id, weight, height = "";
        var poke_name = $("input[name='poke_eng_name']").val()

        $.get("https://pokeapi.co/api/v2/pokemon/" + poke_name, function(data, status){
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
                }
                $(".detailMainWrap .info_wrap .card_name .poke_types div.icon").css("display", "block")
            }

            if(poke_id != ""){
                poke_flavor(poke_id)
            }

            // 포켓몬 특성 불러오기
            for (let i = 1; i <= abilities.length; i++) {
                var ability_url = abilities[i]["ability"]["url"];

                if(ability_url !== ""){
                    get_ability(ability_url, i);
                    if(i = abilities.length){
                        $("div.card_abilities").css("display", "block")
                    }
                }
            }
            
            
        });
        setTimeout(function() { 
            $("div.loading").removeClass("active");
            console.log("loading")
        }, 1000);

    }
    // 포켓몬 설명 불러오기
    function poke_flavor(poke_id){
        $.get("https://pokeapi.co/api/v2/pokemon-species/" + poke_id, function(data, status){
            if(data.flavor_text_entries){
                var flavor_text = data.flavor_text_entries.filter((info) => info.language.name == "ko")
                if( flavor_text.length ){
                    flavor_text = flavor_text[flavor_text.length-1].flavor_text
                }
                console.log(flavor_text);
                $("div.card_flavor span").text(flavor_text);
            }
        });
    }
    // 포켓몬 특성 불러오기
    function get_ability(url, i){
        $.get(url, function(data, status){
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
        });
    }
    
});
