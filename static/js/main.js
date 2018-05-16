$('#submit-btn').on("click", function() {
    let nameFirst = $("input[name='answer-1']").val()
    let nameSecond = $("input[name='answer-2']").val()
    let nameThird = $("input[name='answer-3']").val()
    let nameFourth = $("input[name='answer-4']").val()
    let nameFifth = $("input[name='answer-5']").val()
    
    $.ajax({
        type: "POST",
        url: "some.php",
        data: {
            answer1: nameFirst,
            answer2: nameSecond,
            answer3: nameThird,
            answer4: nameFourth,
            answer5: nameFifth
        },
        success: function() {
            $('#success').text("Hurray!")
        }
    });
})