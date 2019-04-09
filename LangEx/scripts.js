//list of all default languages and button memory:
var languages = ["Spanish",'Mandarin',
'Japanese','Russian','Bengali ','Portuguese','Arabic' ,
'Punjabi','German','French','Turkish','Italian','Polish',
'Greek','Swedish','Czech','Hungarian'];
languages.sort();
languages = ['English','Dutch'].concat(languages).concat(['other...']);

var proficiencies = {'L': ['B','I','A'],
                  'T': ['A','N']};

var buttonsL = [];
var buttonsT = [];


/* When the user clicks on the button,
toggle between hiding and showing the dropdown content */
function expandDdn(e) {
    var id = (e.target.id).replace("btn", "ddn");
    document.getElementById(id).classList.toggle("show");
  }
  
  // Close the dropdown menu if the user clicks outside of it
  window.onclick = function(event) {
    if (!event.target.matches('.dropbtn')) {
      var dropdowns = document.getElementsByClassName("dropdown-content");
      var i;
      for (i = 0; i < dropdowns.length; i++) {
        var openDropdown = dropdowns[i];
        if (openDropdown.classList.contains('show')) {
          openDropdown.classList.remove('show');
        }
      }
    }
  } 

function add_ddn(learn){

  var id = "section"+learn;
  var div = document.getElementById(id);
  var btn =document.createElement("BUTTON");   // Create a <button> element
  btn.innerHTML = "add language";                   // Insert text
  btn.onclick= function(e){expandDdn(e)};
  btn.setAttribute("class","dropbtn");
  var btnId = ((learn == 'L') ?  "btn"+learn+((buttonsL.length).toString()) : "btn"+learn+((buttonsT.length).toString()));
  btn.setAttribute("id",btnId);
  var p =document.createElement("p");   

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
    label.innerHTML = proficiencies[learn][i]+':';
    radios.appendChild(label);
    //radio.innerHTML(proficiencies[learn][i]);
    radios.appendChild(radio);
  }
  p.appendChild(radios);
  div.appendChild(p);  
  fillContent(learn);
  (learn == 'L') ? buttonsL.push(btnId) : buttonsT.push(btnId);

}

function fillContent(learn){
    var id = "section"+learn;
    var div = document.getElementById(id);
    var ddn = document.createElement("div");
    ddn.setAttribute("class","dropdown-content");
    var ddnId = ((learn == 'L') ?  "ddn"+learn+((buttonsL.length).toString()) : "ddn"+learn+((buttonsT.length).toString()));
    ddn.setAttribute("id",ddnId);
    for (var i =0;i<languages.length;i++){
        var a = document.createElement("a");

        a.onclick= function(e){selectLanguage(e)};
        a.innerHTML = languages[i];

        ddn.appendChild(a);
    }
    div.appendChild(ddn);

}

function selectLanguage(e){
    id = e.target.parentNode.id.replace("ddn", "btn");
    if (document.getElementById(id).innerHTML==="add language"){
        var learn = id[3];
        add_ddn(learn)
    };
    document.getElementById(id.replace("btn","radios" )).style.display = "inline";//.toggle("show");
    document.getElementById(id).innerHTML = e.target.innerHTML;
}


