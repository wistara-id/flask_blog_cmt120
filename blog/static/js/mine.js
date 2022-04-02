/* Script to light up the navigation menu based on URL of visited page
*
* This code was adapted from Stack Overflow answer by Sergey Bezugliy 03-06-2018
* accessed 21-01-2022
* https://stackoverflow.com/questions/20060467/add-active-navigation-class-based-on-url
* 
* The adapted code is modified to cater the active class of the blog website menu
* 
*/
$(document).ready(function () {
    $.each($('.nav-item').find('a'), function() {
        if ('/' + $(this).attr('id') == window.location.pathname) {
            $(this).addClass('active')
        }
    });
});