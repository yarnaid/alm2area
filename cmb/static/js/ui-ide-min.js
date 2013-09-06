Ext.onReady(function(){function C(){tree=new Ext.tree.TreePanel({autoScroll:true,animate:true,containerScroll:true,border:false,enableDD:true,useArrows:true,dataUrl:"tree-data.json.php",root:{nodeType:"async",text:"Files",draggable:false,id:m},listeners:{click:function(a){if(a.leaf){q=a.attributes.url;r(q)}},contextmenu:function(a,b){a.select();context_menu.node=a;context_menu.show(b.getTarget())}}});tree.getRootNode().expand();n.add(tree);n.setActiveTab(0)}function o(a,b){var c=a.replace(/^.*[\/\\]/g, "");j.add({title:c,id:b,iconCls:"tabs",html:"<textarea id=textarea_"+b+"> </textarea>",closable:true,listeners:{beforeclose:function(h){if(f[b].getCode()!=localStorage.getItem(b)){Ext.Msg.show({title:"Save Changes?",msg:"You are closing a tab that has unsaved changes. Would you like to save your changes?",buttons:Ext.Msg.YESNOCANCEL,fn:function(k){if(k=="yes"){s(b);delete f[b];j.remove(h)}else if(k=="no"){delete f[b];j.remove(h)}},animEl:"elId",icon:Ext.MessageBox.QUESTION});return false}}}}).show(); c=["codemirror/xmlcolors_on_white.css","codemirror/jscolors_on_white.css","codemirror/csscolors_on_white.css"];var e=["parsexml.js","parsecss.js","tokenizejavascript.js","parsejavascript.js","parsehtmlmixed.js"],d={};switch(""+(/[.]/.exec(a)?/[^.]+$/.exec(a):undefined)){case "js":c=["codemirror/jscolors_on_white.css"];e=["tokenizejavascript.js","parsejavascript.js"];break;case "css":c=["codemirror/csscolors_on_white.css"];e=["parsecss.js"];break;case "py":c=["codemirror/pythoncolors.css"];e=["parsepython.js"]; d={pythonVersion:2,strictErrors:true}}f[b]=CodeMirror.fromTextArea("textarea_"+b,{stylesheet:c,parserfile:e,path:"codemirror/",autoMatchParens:true,height:"100%",content:localStorage.getItem(b),textWrapping:false,lineNumbers:true,indentUnit:4,breakPoints:false,iframeClass:"editorCode",parserConfig:d})}function t(){l("save")}function u(){window.location="/open"}function v(){Ext.Msg.prompt("Keywords","Please enter text to find:",function(a,b){if(a=="ok"&&!w(b)){Ext.getBody().mask("Searching...","x-mask-loading"); Ext.Ajax.request({url:"model_editor.php",params:{cmd:"find",keywords:b,workingcopy:g},success:function(c){c=Ext.util.JSON.decode(c.responseText);x.store.loadData(c);Ext.getBody().unmask();y.expand(true)},failure:function(){Ext.getBody().unmask()}})}})}function z(a,b){b&&A(a.value)}function D(){for(var a in f)s(a)}function s(a){f.hasOwnProperty(a)&&f[a].getCode()!=localStorage.getItem(a)&&localStorage.setItem(a,f[a].getCode())}function r(a){function b(e){e.each(function(d){localStorage.setItem(d.get("id"), d.get("content"));d=d.get("id");document.getElementById(d)==null&&o(a,d)})}var c=encodeURIComponent(a);if(null==localStorage.getItem(c))(new Ext.data.JsonStore({url:"/model_editor.php",fields:["id","content"],listeners:{load:b}})).load({params:{cmd:"getData",path:a}});else document.getElementById(c)==null&&o(a,c)}function l(a){switch(a){case "load":Ext.getBody().mask("Loading project...","x-mask-loading");Ext.Ajax.request({url:"model_editor.php",params:{cmd:"getMeta",workingcopy:g},success:function(c){metaServer= c.responseText;c=localStorage[g+"_meta"];c!=metaServer&&Ext.Ajax.request({url:"model_editor.php",params:{cmd:"getData",workingcopy:g,meta:c},success:function(e){e=Ext.util.JSON.decode(e.responseText);for(var d in e)localStorage.setItem(d,e[d]);localStorage[g+"_meta"]=metaServer;for(var h in f)f[h].getCode()!=localStorage.getItem(h)&&f[h].setCode(localStorage.getItem(h))}})},failure:function(){Ext.Msg.alert("Sync","Offline mode: It is not possible to connect to server, there may be connection problems, please try again later")}}); break;case "save":Ext.getBody().mask("Saving project...","x-mask-loading");var b=E();D();Ext.Ajax.request({url:"model_editor.php",params:{cmd:"getMeta",workingcopy:g},success:function(c){metaServer=c.responseText;c=localStorage[g+"_meta"];if(c==metaServer){c=c.length==0?{}:Ext.util.JSON.decode(c);for(var e={},d=0;d<b.length;d++){if(b[d]in c)c[b[d]]++;else c[b[d]]=0;e[b[d]]=localStorage.getItem(b[d])}if(!w(e)){var h=Ext.util.JSON.encode(c);c=Ext.util.JSON.encode(e);Ext.Ajax.request({url:"model_editor.php", params:{cmd:"setMetaAndData",workingcopy:g,meta:h,data:c},success:function(){localStorage[g+"_meta"]=h;localStorage.removeItem("IdsModifiedFiles")},failure:function(){Ext.Msg.alert("Sync","It is not possible to connect to server, try again later")}})}}else Ext.Msg.show({title:"Reload reload remote changes",msg:"There are remote changes. Would you like reload your project with this changes?",buttons:Ext.Msg.YESNOCANCEL,fn:function(k){if(k=="yes")l("load");else k=="no"&&l("save")},animEl:"elId",icon:Ext.MessageBox.QUESTION})}, failure:function(){Ext.Msg.alert("Sync","Offline mode: It is not possible to connect to server, try again later")}})}Ext.getBody().unmask()}function E(){var a=Ext.util.JSON.decode(localStorage.getItem("IdsModifiedFiles"));a=a!=null?a:[];for(var b in f)b in a==false&&f[b].getCode()!=localStorage.getItem(b)&&a.push(b);localStorage.setItem("IdsModifiedFiles",Ext.util.JSON.encode(a));return a}function w(a){for(var b in a)if(a.hasOwnProperty(b))return false;return true}function A(a){var b,c,e=document.getElementsByTagName("link"), d=e.length;for(b=0;b<d;b++){c=e[b];if(c.getAttribute("rel").indexOf("style")!=-1&&c.getAttribute("title")){c.disabled=true;if(c.getAttribute("title")==a)c.disabled=false}}}window.onbeforeunload=function(){for(var a in f)if(f[a].getCode()!=localStorage.getItem(a))return"There are unsaved changes, press cancel if you want save your changes before exit"};A("gray");var n,g,m,i;Ext.Ajax.timeout=24E4;if(window.location.pathname=="/open"){var B=new Ext.FormPanel({labelAlign:"right",labelWidth:85,waitMsgTarget:true, frame:true,defaultType:"textfield",items:[new Ext.form.ComboBox({fieldLabel:"Version control",hiddenName:"vcCmd",store:new Ext.data.ArrayStore({fields:["vc","vcCmd"],data:[["Mercurial","hg clone"],["Git","git clone"],["Subversion","svn co"]]}),valueField:"vcCmd",displayField:"vc",typeAhead:true,mode:"local",triggerAction:"all",emptyText:"Select a version control client...",selectOnFocus:true,width:190}),new Ext.form.Hidden({name:"cmd",value:"checkOut"}),{fieldLabel:"Url",emptyText:"http://...",name:"url", width:190},{fieldLabel:"Working copy",emptyText:"My working copy",id:"workingcopy",name:"workingcopy",width:190}]});i=function(){B.getForm().submit({url:"model_editor.php",waitMsg:"Checking out...",submitEmptyText:false,timeout:240,success:function(){g=Ext.getCmp("workingcopy").getValue();m="workingcopies/"+g;window.location=g;p.close()},failure:function(a,b){Ext.Msg.alert("Failure",b.result.msg)}})};var F=new Ext.Button({text:"Submit",disabled:false,handler:i});new Ext.KeyMap(Ext.getDoc(),{key:Ext.EventObject.ENTER, fn:i,scope:this});var p=new Ext.Window({title:"Checkout project",minimizable:false,maximizable:false,width:330,height:150,layout:"fit",border:false,buttonAlign:"center",items:B,buttons:[F,{text:"Cancel",handler:function(){p.close()}}]});p.show();i=true}else{i=false;g=window.location.pathname.split("/")[1];m=window.location.pathname!="/edit"?"workingcopies"+window.location.pathname:".";l("load")}new Ext.KeyMap(Ext.getDoc(),[{key:"f",ctrl:true,shift:true,stopEvent:true,fn:function(){v()}},{key:"o", ctrl:true,stopEvent:true,fn:function(){u()}},{key:"s",ctrl:true,stopEvent:true,fn:function(){t()}}]);var f=[],j=new Ext.TabPanel({resizeTabs:true,minTabWidth:115,tabWidth:135,enableTabScroll:true,width:600,height:250,defaults:{autoScroll:true},region:"center",deferredRender:false,activeTab:0});(new Ext.Button({text:"Add Tab",handler:o,iconCls:"new-tab"})).render(document.body,"tabs");var q="",x=new Ext.grid.GridPanel({store:new Ext.data.ArrayStore({fields:["context","location"],idIndex:0}),colModel:new Ext.grid.ColumnModel({defaults:{sortable:true}, columns:[{header:"Context",dataIndex:"context"},{header:"Location",dataIndex:"location"}]}),viewConfig:{forceFit:true,getRowClass:function(a){a=a.get("change");if(a<0)return"par";else if(a>0)return"impar"}},sm:new Ext.grid.RowSelectionModel({singleSelect:true}),title:"Search",iconCls:"icon-grid",listeners:{rowclick:function(a,b){var c="workingcopies/"+g+"/"+a.store.getAt(b).get("location");r(c)}}}),y=new Ext.Panel({region:"south",contentEl:"south",split:true,collapsed:true,height:200,maxSize:300, collapsible:true,title:"Console",margins:"0 0 0 0",layout:"fit",items:new Ext.TabPanel({border:false,activeTab:0,tabPosition:"bottom",items:[x]})});new Ext.Viewport({layout:"border",items:[new Ext.Toolbar({height:32,region:"north",items:[{text:"Files",menu:[{text:"Open Project\t(Ctrl+O)",handler:u},{text:"Save Project\t(Ctrl+S)",handler:t}]},{text:"Edit",menu:[{text:"Format Selection\t(Tab)",handler:function(){f[j.getActiveTab().id].reindentSelection()}},{text:"Find in project\t(Ctrl+Shift+F)",handler:v}]}, {text:"Style",menu:{items:['<b class="menu-title">Choose a Theme</b>',{text:"Gray Theme",value:"gray",checked:true,group:"theme",checkHandler:z},{text:"Aero Glass",value:"blue",checked:false,group:"theme",checkHandler:z}]}}]}),y,{region:"east",title:"Properties",collapsible:true,split:true,width:225,minSize:175,maxSize:400,margins:"0 5 0 0",layout:"fit",items:new Ext.TabPanel({border:false,activeTab:0,tabPosition:"bottom",items:[new Ext.grid.PropertyGrid({title:"Property Grid",closable:true,source:{name:"test", "read only":false,created:new Date(Date.parse("10/15/2006")),Modified:false,version:0.01}})]})},{region:"west",id:"west-panel",title:"Project Explorer",split:true,width:200,minSize:175,maxSize:400,collapsible:true,margins:"0 0 0 5",layout:{type:"accordion",animate:true},items:n=new Ext.TabPanel({border:false,tabPosition:"bottom"})},j]});if(!i){C();Ext.getBody().unmask()}});
