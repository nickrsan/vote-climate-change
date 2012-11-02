/**
 * Created with PyCharm.
 * User: Nick
 * Date: 10/2/12
 * Time: 10:04 PM
 */
$(function () {

	$(".unimplemented").click(function (event) {
		$("div#unimplemented_msg").dialog({
			modal: true,
			width: 450,
			buttons: {
				Close: function() {
					$( this ).dialog( "close" );
				}
			}
		});
		event.preventDefault();
		return false;
	});

	var slider = $("#facts_slider");
	slider.orbit({ fluid: '2x1', animationSpeed: 400, advanceSpeed: 10000, bullets: true, directionalNav: false});
	slider.children("div.fact_statement").first().css("left", 0); // bring the first fact back into view
    set_find_electable('input#candidate');

	set_addition_triggers("#add_items");

	var form_container = "form#publisher";
	set_ajax_submit(form_container);

	$.backstretch('/static/background_nasa_1600_black50_blur.jpg');
	//set_file_drop();

	$( "div#action_box" ).dialog({
		modal: true,
		autoOpen: false,
		width: 450,
		buttons: {
			Close: function() {
				$( this ).dialog( "close" );
			}
		}
	});
});

function set_ajax_submit(form_container){
	var submit_obj = $(form_container);
	submit_obj.submit(
		function(event){
			submit_statement(form_container);
			event.preventDefault();
		}
	);

}

function set_file_drop() {
    var url = '/upload/image/';
    var fdid = 'image_filedrop';
	// Tell FileDrop we can deal with iframe uploads using this URL:
	var options = {iframe: {url: url},dragOverClass:'drag_enter'};
	// Attach FileDrop to an area:
	var zone = new FileDrop(fdid, options);

	// Do something when a user chooses or drops a file:
	zone.on.send.push(function (files) {
		// if browser supports files[] will contain multiple items.
		for (var i = 0; i < files.length; i++) {
			files[i].SendTo(url);
		}
	});

    //zone.on[fileSetup].push(function(file){
    //    $('#' + fdid).append('<p>'+ file.filename + '</p>');//<img src="' + file.nativeFile + '">');
    //});

}

function trigger_action(event_target) {

	var target_attribute = $(event_target).attr('data-trigger');
	var target_container = $('div#' + target_attribute);
	if ($(event_target).hasClass('selected')) {
		$(event_target).removeClass('selected');
		if (target_container.attr('id') === "text_addition_container"){
			$("textarea#text_addition").attr("disabled","disabled");
		}
		target_container.slideUp();
	} else {
		if (target_container.attr('id') === "text_addition_container"){
			$("textarea#text_addition").removeAttr("disabled");
		}
		$(event_target).addClass('selected');
		target_container.slideDown();
	}
}

function set_addition_triggers(container){
	var trigger_items = $(container + " li a.trigger");
	trigger_items.click(function(event){
		trigger_action(event.target);
		event.preventDefault();
	});
}

function submit_statement(form_container){
	var url = '/publish/';
	var success_func = submit_success;
	$.ajax({
		type: 'POST',
		url: url,
		data: $(form_container).serialize(),
		success: submit_success,
		dataType: 'json',
		error: submit_error,
		beforeSend: submit_setup,
	});
}

function submit_setup(jqXHR,settings){
	$("#error_box").hide();
}

function submit_error(jqXHR,textStatus,errorThrown){
	var error_box = $("#error_box");
	error_box.text("Error: " + jqXHR.responseText + ". If this error doesn't make sense, rest assured we're working on it.");
	error_box.show();
}

function submit_success(data, textStatus, jqXHR){
	if (data.status === "success") {
		$( "#action_box").dialog("open");
		add_to_page(data.data);
	}else if(data.status === "error") {
		submit_error(jqXHR,textStatus,data.data);
	}
}

function add_to_page(rendered_html){
	var after_target = $("div#statements h3");
	after_target.after("<div class=\"new_insert\">" + rendered_html + "</div>");
	$("div.new_insert").show('swing');
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

            var state_field = $("input#state");
            var state_val = state_field.val()
            var support_type = $("select#support_style");
            if((state_val === undefined || state_val === '')
                && support_type.val() === "I'm voting for"){
                state_field.val(ui.item.state_abbrev);
            }
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


/**
 * syncHeight - jQuery plugin to automagically Snyc the heights of columns
 * Made to seemlessly work with the CCS-Framework YAML (yaml.de)
 * @requires jQuery v1.0.3
 *
 * http://blog.ginader.de/dev/syncheight/
 *
 * Copyright (c) 2007-2009
 * Dirk Ginader (ginader.de)
 * Dirk Jesse (yaml.de)
 * Dual licensed under the MIT and GPL licenses:
 * http://www.opensource.org/licenses/mit-license.php
 * http://www.gnu.org/licenses/gpl.html
 *
 * Version: 1.2
 *
 * Usage:
 $(window).load(function(){
$('p').syncHeight();
});
 */

(function($) {
	var getHeightProperty = function() {
		var browser_id = 0;
		var property = [
// To avoid content overflow in synchronised boxes on font scaling, we
// use 'min-height' property for modern browsers ...
			['min-height','0px'],
// and 'height' property for Internet Explorer.
			['height','1%']
		];

// check for IE6 ...
		if($.browser.msie && $.browser.version < 7){
			browser_id = 1;
		}

		return { 'name': property[browser_id][0],
			'autoheightVal': property[browser_id][1] };
	};

	$.getSyncedHeight = function(selector) {
		var max = 0;
		var heightProperty = getHeightProperty();
// get maximum element height ...
		$(selector).each(function() {
// fallback to auto height before height check ...
			$(this).css(heightProperty.name, heightProperty.autoheightVal);
			var val = $(this).height();
			if(val > max){
				max = val;
			}
		});
		return max;
	};

	$.fn.syncHeight = function(config) {
		var defaults = {
			updateOnResize: false,	// re-sync element heights after a browser resize event (useful in flexible layouts)
			height: false
		};
		var options = $.extend(defaults, config);

		var e = this;

		var max = 0;
		var heightPropertyName = getHeightProperty().name;

		if(typeof(options.height) === "number") {
			max = options.height;
		} else {
			max = $.getSyncedHeight(this);
		}
// set synchronized element height ...
		$(this).each(function() {
			$(this).css(heightPropertyName, max+'px');
		});

// optional sync refresh on resize event ...
		if (options.updateOnResize === true) {
			$(window).resize(function(){
				$(e).syncHeight();
			});
		}
		return this;
	};
})(jQuery);