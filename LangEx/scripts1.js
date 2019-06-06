//list of all default languages and button memory:
var languages = ["Spanish",'Mandarin',
'Japanese','Russian','Bengali ','Portuguese','Arabic' ,
'Punjabi','German','French','Turkish','Italian','Polish',
'Greek','Swedish','Czech','Hungarian'];
languages.sort();
languages = ['English','Dutch'].concat(languages).concat(['other...']);

//Proficiency levels for teaching/learning languages;
var proficiencies = {'L': ['B','I','A'],
                  'T': ['A','N']};
var prof_written = {'L': ['beginner','interm.','advanced'],
                  'T': ['advanced','native']};
//stores all Learn/Teach buttons.
var buttonsL = [];
var buttonsT = [];


function getRadioVal(radios) {
  var val;
  // alert(radios.childNodes.length)

  // loop through list of radio buttons
  for (var i=0, len=radios.childNodes.length; i<len; i++) {
      if (radios.childNodes[i].checked ) { // radio checked?
          val = radios.childNodes[i].value; // if so, hold its value in val
          break; // and break out of for loop
      }
  }
  return val; // return value of checked radio or undefined if none checked
}

//add a new dropdown menu to 'teach' (arg="T") or 'learn' (arg="L")
function add_ddn(learn){

    var id = "section"+learn;                     //find the correct section
    var div = document.getElementById(id);        
    var btn =document.createElement("select");   // Create a <button> element

    var btnId = ((learn == 'L') ?  "btn"+learn+((buttonsL.length).toString()) : "btn"+learn+((buttonsT.length).toString()));
    btn.setAttribute("id",btnId);

    btn.onchange= function(e){selectLanguage(e)};
    btn.setAttribute("class","dropbtn");
    btn.topmost = true

    var btnId = ((learn == 'L') ?  "btn"+learn+((buttonsL.length).toString()) : "btn"+learn+((buttonsT.length).toString()));
    btn.setAttribute("id",btnId);
    var p =document.createElement("p"); 

    var option = document.createElement('option');
    option.text = 'add language';
    option.selected = true;
    option.disabled = true;
    option.hidden = true;
    btn.add(option);

    for (var i=0;i<languages.length;i++){
        var option = document.createElement('option');
        option.text = languages[i];
        btn.add(option);
    }

    p.appendChild(btn);  


  
  var radios = document.createElement("div");
  radios.className = "radios";
  radios.id = "radios"+learn+((((learn == 'L') ?  buttonsL.length : buttonsT.length).toString()));
  
  var len = ((proficiencies[learn]).length);
    for (var i =0;i<len;i++){
      var radio = document.createElement('input');
      radio.setAttribute('type', 'radio');
      if (!i) {radio.setAttribute("checked","checked")};
    radio.setAttribute('name','prof'+learn+(((learn == 'L') ?  buttonsL : buttonsT).length).toString());
    radio.setAttribute('value',proficiencies[learn][i]);
    var label = document.createElement("label");
    label.setAttribute("for",radio.id);
    label.innerHTML = prof_written[learn][i];
    radios.appendChild(label);

    radios.appendChild(radio);
  }
  var inputBox = document.createElement('input');
  inputBox.setAttribute('type','text');
  inputBox.setAttribute('name','other'+learn+(((learn == 'L') ?  buttonsL : buttonsT).length).toString());
  inputBox.defaultValue='other language...';
//   fillContent(learn);

  p.appendChild(radios);
 
  p.appendChild(inputBox);
  div.appendChild(p);  
  (learn == 'L') ? buttonsL.push(btnId) : buttonsT.push(btnId);

}



//listens to events from the language dropdown menu.
function selectLanguage(e){

    id = e.target.id;
    // alert(e.target.selectedOptions[0].value)
    var option = e.target.selectedOptions[0].value;

    if (e.target.topmost)
    {
        var learn = id[3];
         add_ddn(learn);
         e.target.topmost=false;
  };  
  if (option==="other..."){
    document.getElementsByName(id.replace("btn","other" ))[0].style.display = "inline";
  }
  else{
    document.getElementsByName(id.replace("btn","other" ))[0].style.display = "none";
  }

    document.getElementById(id.replace("btn","radios" )).style.display = "inline";
    // document.getElementById(id).innerHTML = e.target.innerHTML;    
    document.getElementById(id).style.backgroundColor = "rgb( 73,175, 55)";
}

function reset(){
    location.reload(); 
}

function submit(){

  const data = new FormData();

  const personal_info = {}

  var item_list = ((document.getElementsByClassName("headerbox")));
  if (!item_list[2].value.includes("@")){
    alert("Please enter a valid e-mail address!");
    return;
  }

  for (let item of item_list){
    if (item.value === ""){
      alert("Please fill out your personal contact information.");
      return;
    }
    else{
      personal_info[item.id]=item.value
    }
  }    


  langs_learn = {};

  if (buttonsL.length==1){
    alert("Please select at least one language to practice.");
    return;
  };

  var text="";
  for (let item of buttonsL){
    text = (document.getElementById(item).selectedOptions[0].value);
    if (text==="add language"){
      break;
    }
    else if (text==="other..."){
      var textId = item.replace("btn","other");
      var text = (document.getElementsByName(textId)[0].value);
      switch (text){
        case "":{
          alert ("Please fill in your 'other' language.");
        return;}
        case "other language plz :)":{
          alert ("Please fill in your 'other' language.");
        return;}
      default:{
        true;
      }
      }
    }
    else {
      // data.push(text);
    }

    langs_learn[text] = (getRadioVal(document.getElementById(item.replace("btn","radios"))));
  }

  langs_teach = {};

  if (buttonsT.length==1){
    alert("Please select at least one language to teach.");
    return;
  };

  for (let item of buttonsT){
    text = (document.getElementById(item).selectedOptions[0].value);
    if (text==="add language"){
      break;
    }
    else if (text==="other..."){
      var textId = item.replace("btn","other");
      var text = (document.getElementsByName(textId)[0].value);
      switch (text){
        case "":{
          alert ("Please fill in your 'other' language.");
        return;}
        case "other language...":{
          alert ("Please fill in your 'other' language.");
        return;}
      default:{
        true;
      }
      }
    }
    langs_teach[text] = (getRadioVal(document.getElementById(item.replace("btn","radios"))));

  }

  const xhr = new XMLHttpRequest();
  // const xhr_get = new XMLHttpRequest();


  data.append('input',JSON.stringify({'personal_info':personal_info,
                                        'langs_learn':langs_learn,
                                      'langs_teach':langs_teach}));


  const handleResponse = ({ target }) => {
    // Do something useful here...

    if (target.readyState === XMLHttpRequest.DONE) {
      if (target.status === 200) {
        alert(target.responseText);
      } else {
        alert('something broke ....')
      }
    }  }
  
  xhr.addEventListener('message', handleResponse)
  // xhr_get.addEventListener('message', handleResponse)

  xhr.onreadystatechange = handleResponse;

  xhr.open('POST', 'http://127.0.0.1:5000/api');
  // xhr_get.open('GET', 'http://127.0.0.1:5000/api');
  
  xhr.send(data);
  // xhr_get.send(data);

  // var i=0
  // while (i<4){
  //   alert('_'+xhr_get.readyState+'_'+xhr_get.status+'_'+xhr_get.responseText)
  //   i=i+1;
  // }
}
