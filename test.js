//카디널레드
var intervalId = setInterval (function() {
    var element = document.evaluate(
        '//*[@id="content-1"]/div/div/div[2]/div[5]/p',
        document,
        null,
        XPathResult.FIRST_ORDERED_NODE_TYPE,
        null
      ).singleNodeValue;
      
      // 요소가 존재하고 display 속성 값이 "none"인지 확인
      if (element && getComputedStyle(element).display === "none") {
        var sizeElement = document.evaluate('//*[@id="content-1"]/div/div/div[2]/div[5]/a[1]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null);
        var selectedElement = sizeElement.singleNodeValue;
        if (selectedElement) {
            clearInterval(intervalId);
            selectedElement.click();
        }
      } else {
        setTimeout(() => location.reload(),2000);
        
        }
}, 100);

var intervalId2 = setInterval (function() {
    //무통장입금명 넣기
    var sizeElement2 = document.evaluate('//*[@id="pname"]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null);
    var selectedElement = sizeElement2.singleNodeValue;
    if (selectedElement) {
    selectedElement.value = '진민강'
    }
    
    // 옵션 선택
    var optionIndex = 1; // 0부터 시작하는 인덱스
    var selectElement3 = document.getElementById("bankaccount");
    
    if (selectElement3 && optionIndex >= 0 && optionIndex < selectElement3.options.length) {
        selectElement3.selectedIndex = optionIndex;
    }
    //동의
    var sizeElement4 = document.evaluate('//*[@id="chk_purchase_agreement0"]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null);
    var selectedElement = sizeElement4.singleNodeValue;
    if (selectedElement) {
    selectedElement.click();
    }
    //결제하기
    var sizeElement5 = document.evaluate('//*[@id="btn_payment"]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null);
    var selectedElement = sizeElement5.singleNodeValue;
    if (selectedElement) {
    selectedElement.click();
    }
    clearInterval(intervalId2);
    }, 100);