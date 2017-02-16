$(document).ready(function() {
    $("li#Home").click(function() {
        window.location.href = "/";
    });
    $("li#Login").click(function() {
        window.location.href = "/login";
    });
    $("li#Logout").click(function() {
        window.location.href = "/logout";
    });
    $("li#Signup").click(function() {
        window.location.href = "/signup";
    });
    $("li#MyStudents").click(function() {
        window.location.href = "/mystudents";
    });
});
