function Success(type,text='You clicked the button!'){
    Swal.fire(
        type,
        text,
        'success'
    )
}

function CheckSubmit(){
    let account = document.getElementById("form2Example11").value.length;
    let password = document.getElementById("form2Example22").value.length;
    if (account == 0 && password == 0 ){
      alert("請輸入資料");
      return false
    }
    else if (account == 0 ){
      alert("請輸入帳號");
      return false
    }
    else if (password == 0 ){
      alert("請輸入密碼");
      return false
    }
    else{
      return true
    }
  }