/**
 * Created with PyCharm.
 * User: Nick
 * Date: 10/2/12
 * Time: 10:04 PM
 */

$(function () {
    $("#publish_button").click(function (target, event) {
        publish();
        event.preventDefault();
    });

    $("#facts_slider").orbit({ fluid: '2x1' , animationSpeed:400, advanceSpeed:10000, bullets:true,directionalNav:false});

    set_find_electable('input#candidate');
});

function publish(){
    var publisher = $("#publisher");
}

function set_find_electable(selector){
    $( selector ).autocomplete( {
        source: function( request, response ){
            $.ajax({
                url: "/electable/find/" + request.term + "/",
                dataType: "jsonp",
                minLength: 4,
                autoFocus: true,
                success: function( data ) {
                    response( $.map( data.electables, function( item ) {
						var state_append = ""
						if ( !(item.state_abbrev === 'undefined' || item.state_abbrev === null)) {
							state_append = " (" + item.state_abbrev + ")";
						}

                        return {
                            label: highlight_terms(item.name, request.term) + state_append,
                            value: item.name,
                            cand_id: item.cand_id,
                            state_abbrev: item.state_abbrev,
                            twitter_handle: item.twitter_handle,
                            congresspedia_url: item.congresspedia_url,
                            gender: item.gender,
                        }
                    }));
                }
            });
        },
        select: function(event, ui) {
            change_gender(ui.item.gender);

            $("input#candidate_id").val(ui.item.cand_id);

            //if(!(typeof ui.item.state === 'undefined')){
            $("input#state").val(ui.item.state_abbrev);
            //}
        }
    }).data( "autocomplete" )._renderItem = function( ul, item ) {
        return $( "<li>" )
            .data( "item.autocomplete", item )
            .append( "<a>" + item.label + "</a>" )
            .appendTo( ul );
    };
}

function highlight_terms(name,terms){
    search_terms = terms.split(" "); // split at space
    for(var i=0;i<search_terms.length;i++){

        //check if any of the split items are zero length (ie, when we have a double space or a space at the end. For
        // some reason, this makes jquery ui not process the tags, so we need to skip them.
        if (search_terms[i].length === 0){
            continue;
        }
        var re = new RegExp("(" + search_terms[i] + ")","ig");
        name = name.replace(re,"_-_$1_--_"); //place temporary placeholders so that when parts of the search match "strong" we don't overwrite them
    }
    name = name.replace(/_-_/g,"<strong>"); // fill in the placeholders
    name = name.replace(/_--_/g,"</strong>");
    return name
}

function change_gender(gender){
    var fade_time =500;
    var male_selector = "span#gender_he";
    var female_selector = "span#gender_she";
	var or_selector = "span#gender_or";

    console.log("[" + gender + "]");

    if (!(typeof gender === 'undefined' || gender === '' || gender === null)){
        $(or_selector).fadeOut(fade_time);
        if (gender == "M"){
            $(male_selector).fadeIn(fade_time);
            $(female_selector).fadeOut(fade_time);
        }else if(gender == "F"){
            $(male_selector).fadeOut(fade_time);
            $(female_selector).fadeIn(fade_time);
        }
    }else{
		$(or_selector).fadeIn(fade_time);
		$(female_selector).fadeIn(fade_time);
		$(male_selector).fadeIn(fade_time);
	}
}


