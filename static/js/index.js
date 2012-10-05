/**
 * Created with PyCharm.
 * User: Nick
 * Date: 10/2/12
 * Time: 10:04 PM
 */

$().ready(function () {
    $("#publish_button").click(function (target, event) {
        publish();
        event.preventDefault();
    });

    $("#facts_slider").orbit({ fluid: '2x1' , animationSpeed:400, advanceSpeed:10000, bullets:true,directionalNav:false});

});

function publish(){
    var publisher = $("#publisher");
}