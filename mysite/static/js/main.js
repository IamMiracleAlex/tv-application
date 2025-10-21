
// Carousel functions 

//define parameters
let image_stack = $(".images");
let right_control = $(".fa-angle-right");
let left_control = $(".fa-angle-left");
let init = 0;
// let right_control set next image active and remove active from current one

right_control.on("click", function () {
    let active_img = $(".active_img");
    let next_slide = $(active_img.next());
    let next_slide2 = $(next_slide.next());
    let next_slide3 = $(next_slide2.next());
    if (init > image_stack.length - 2) {
        console.log("This is the last image");
        $(image_stack[image_stack.length -1]).addClass("active_img");

    } else {
        active_img.removeClass("active_img");
        next_slide.addClass("active_img").removeClass("img_container_2");
        next_slide2.addClass("img_container_2").removeClass("img_container_3");
        next_slide3.addClass("img_container_3");
        init = init + 1;

    }
})


// let left_control set previous image active and remove active from current one
left_control.on("click", function () {
    let active_img = $($(".active_img"));
    let prev_slide = $(active_img.prev());
    let next_slide = $(prev_slide.next());
    let next_slide2 = $(next_slide.next());
    let next_slide3 = $(next_slide2.next());

    if (init === 0) {
        console.log("This is First image");
    }
    else {
        prev_slide.addClass("active_img");
        next_slide.removeClass("active_img").addClass("img_container_2");
        next_slide2.removeClass("img_container_2").addClass("img_container_3");
        next_slide3.removeClass("img_container_3");
        init = init - 1;

    }
})


//   Effect on sort movies
let myDropdown = $(".myDropdown");
let dropdown_content = $(".dropdown_content");
let dropdown_content_items = dropdown_content.children();
myDropdown.on("click", function () {
    dropdown_content.toggle();

    for (i = 0; i < dropdown_content_items.length; i++) {
        $(dropdown_content_items[i]).on("click", function () {
            let value_source = $(this).text();
            $(".myDropdown .filter_value").text(value_source);

            $(".check_state").css("display", "none");
            $(".active_check").removeClass("active_check")
            $(this).children("span").css("display", "block");
            dropdown_content.css("display", "none");
        })
    }
})


// effects on movie lists
let state_icon = $(".state_icon");
let primary_state = $(".m_state .icons");
let saw_movie = $(".fa-check");
let watch_movie = $(".movie_tag");
for (i = 0; i < state_icon.length; i++) {

    $(state_icon[i]).css("cursor", "pointer").on("click", function () {
        $(this).toggleClass("active_state_icon");
        primary_state.css("z-index", "1")
    })

}

$(saw_movie).on("click", function () {
    let b = $(this).parents(".m_state").siblings(".seen").toggleClass("display_flex");
})

$(watch_movie).on("click", function () {
    $(this).parents(".m_state").siblings(".watch").toggleClass("display_flex");
    let b = $(this).parent().toggleClass("moveup");
})

//SIDEBAR FUNCTION 
let arrow = $(".arrow");
let sidebar = $(".sidebar");
arrow.on("click", function () {
    $(this).toggleClass("fa-arrow-right").css("right", "-15px !important");
    $(sidebar).toggleClass("toggleSidebar");

})

