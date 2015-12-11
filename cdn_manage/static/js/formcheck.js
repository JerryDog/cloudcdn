
	v = new Array();
	t = new Array();
	c = new Array();
	v[101] = "楠岃瘉鐮侀敊璇紒";
	t[101] = "";
	c[101] = "";

	v[102] = "閫氳璇佹垨瀵嗙爜涓嶈兘涓虹┖锛�";
	t[102] = "";
	c[102] = "";

	v[103] = "闈炴硶鐨剅eturn_url!";
	t[103] = "";
	c[103] = "";

	v[104] = "楠岃瘉璇锋眰寮傚父!";
	t[104] = "";
	c[104] = "";

	v[105] = "閿欒鐨勭敤鎴峰悕鎴栧瘑鐮�!";
	t[105] = "";
	c[105] = "";

	v[106] = "鐧诲綍寮傚父!";
	t[106] = "";
	c[106] = "";

	v[107] = "淇濆瓨DB鍑洪敊锛岃鑱旂郴绠＄悊鍛�!";
	t[107] = "";
	c[107] = "";

	v[108] = "鐭俊閫氶亾寮傚父!";
	t[108] = "";
	c[108] = "";

	v[109] = "鎵嬫満鍙风爜閿欒!";
	t[109] = "";
	c[109] = "";

	v[110] = "鎵嬫満楠岃瘉鐮佷笉鑳戒负绌�!";
	t[110] = "";
	c[110] = "";

	v[111] = "鎭枩鎮紒娉ㄥ唽鎴愬姛锛�";
	t[111] = "";
	c[111] = "";

	v[112] = "娉ㄥ唽澶辫触锛�";
	t[112] = "";
	c[112] = "";

	v[113] = "鐭俊鏈嶅姟閫氶亾寮傚父锛岃绋嶅€欏啀璇曪紒";
	t[113] = "";
	c[113] = "";

	v[114] = "鎮ㄧ殑鎿嶄綔杩囦簬棰戠箒锛屽彂閫侀獙璇佺爜澶辫触锛岃绋嶅€欏啀璇曪紒";
	t[114] = "";
	c[114] = "";

	v[115] = "鐭俊楠岃瘉鐮佸凡鍙戦€佽嚦鎮ㄧ殑鎵嬫満锛岃鎮ㄦ敞鎰忔煡鏀讹紒";
	t[115] = "";
	c[115] = "";

	v[116] = "鎮ㄥ～鍐欑殑鎵嬫満楠岃瘉鐮侀敊璇紒";
	t[116] = "";
	c[116] = "";

	v[117] = "娉ㄥ唽淇濆瓨鏁版嵁澶辫触锛岃绋嶅€欏啀璇曪紒";
	t[117] = "";
	c[117] = "";

	v[118] = "璇ヨ处鍙峰凡缁忔敞鍐岃繃锛�";
	t[118] = "";
	c[118] = "";

	v[119] = "璐﹀彿闀垮害涓嶈兘灏忎簬6浣嶆垨澶т簬46浣嶏紒";
	t[119] = "";
	c[119] = "";

	v[120] = "瀵嗙爜闀垮害涓嶈兘灏忎簬6浣嶆垨澶т簬16浣嶏紒";
	t[120] = "";
	c[120] = "";

	v[121] = "鐭俊鏉℃暟宸茶秴杩囨渶澶ч檺鍒讹紝璇锋槑澶╁啀璇曪紒";
	t[121] = "";
	c[121] = "";

	//checkLogin
	v[201] = "璇ュ笎鍙峰凡缁忚娉ㄥ唽锛�";
	t[201] = "";
	c[201] = "";

	//DevelopManage

	v[301] = "娣诲姞搴旂敤鎴愬姛锛�";
	t[301] = "";
	c[301] = "";

	v[302] = "淇濆瓨鏁版嵁澶辫触锛佽閲嶈瘯锛�";
	t[302] = "";
	c[302] = "";

	v[303] = "淇敼搴旂敤鎴愬姛锛�";
	t[303] = "";
	c[303] = "";

	v[304] = "鍒犻櫎搴旂敤鎴愬姛锛�";
	t[304] = "";
	c[304] = "";



	function __doSubmit(eventTarget, eventArgument)
	{
		var theform;
		if (window.navigator.appName.toLowerCase().indexOf("netscape") > -1)
		{
			theform = document.forms["form1"];
		}
		else
		{
			theform = document.form1;
		}
		var account = theform.usename.value;
		var pwd = theform.password.value;
		if(account==null||account==''){
			alert("璇疯緭鍏ョ櫥褰曡处鍙凤紒");
			$('#submit').removeClass('loading');
			return false;
		}
		if(pwd==null||pwd==''){
			alert("璇疯緭鍏ョ櫥褰曞瘑鐮侊紒");
			$('#submit').removeClass('loading');
			return false;
		}

		theform.eventTarget.value = eventTarget.split("$").join(":");
		theform.eventArgument.value = eventArgument;
		//send(theform);
		$(theform).ajaxSubmit();
	}

	function __doSubmit_reg(eventTarget, eventArgument)
	{

		var theform;
		if (window.navigator.appName.toLowerCase().indexOf("netscape") > -1)
		{
			theform = document.forms["form1"];
		}
		else
		{
			theform = document.form1;
		}
		var account = theform.account.value;
		var pwd = theform.pwd.value;
		var mp = theform.mp.value;
		var mp_code = theform.mp_code.value;
		var code = theform.code.value;

			if(account==null||account==''){
				alert("璇疯緭鍏ョ櫥褰曡处鍙凤紒");
				return false;
			}
			if(pwd==null||pwd==''){
				alert("璇疯緭鍏ョ櫥褰曞瘑鐮侊紒");
				return false;
			}
			if(mp==null||mp==''){
				alert("璇疯緭鍏ユ墜鏈哄彿锛�");
				return false;
			}

			if(mp_code==null||mp_code==''){
				alert("璇疯緭鍏ユ墜鏈虹煭淇￠獙璇佺爜锛�");
				return false;
			}
			if(code==null||code==''){
				alert("璇疯緭鍏ラ獙璇佺爜锛�");
				return false;
			}

		theform.eventTarget.value = eventTarget.split("$").join(":");
		theform.eventArgument.value = eventArgument;
		send(theform);
	}

		function __doSubmit_addlist(eventTarget, eventArgument)
	{
		var theform;
		if (window.navigator.appName.toLowerCase().indexOf("netscape") > -1)
		{
			theform = document.forms["form1"];
		}
		else
		{
			theform = document.form1;
		}
		//var account = theform.account.value;
		var app_name = theform.app_name.value;
		var app_plat = theform.plat_form.value;
		var app_type = theform.app_type.value;
		var app_language = theform.app_language.value;
		var app_mark = theform.app_mark.value;
		//if(account==null||account==''){
			//alert("璇疯緭鍏ョ櫥褰曡处鍙凤紒");
			//return false;
		//}
		if(app_name==null||app_name==''){
			alert("搴旂敤鍚嶇О涓嶈兘涓虹┖锛�");
			return false;
		}
		if(app_plat==null||app_plat==''){
			alert("骞冲彴涓嶈兘涓虹┖锛�");
			return false;
		}
		if(app_type==null||app_type==''){
			alert("搴旂敤绫诲瀷涓嶈兘涓虹┖锛�");
			return false;
		}
		if(app_language==null||app_language==''){
			alert("璇█涓嶈兘涓虹┖锛�");
			return false;
		}
		if(app_mark==null||app_mark==''){
			alert("搴旂敤鎻忚堪涓嶈兘涓虹┖锛�");
			return false;
		}
		theform.eventTarget.value = eventTarget.split("$").join(":");
		theform.eventArgument.value = eventArgument;
		send(theform);
	}

		function __doSubmitMS(eventTarget, eventArgument)
	{
		var theform;
		if (window.navigator.appName.toLowerCase().indexOf("netscape") > -1)
		{
			theform = document.forms["form1"];
		}
		else
		{
			theform = document.form1;
		}
		var mp = theform.mp.value;

		if(mp==null||mp==''){
			alert("璇疯緭鍏ユ墜鏈哄彿鐮侊紒");
			return false;
		}
		theform.eventTarget.value = eventTarget.split("$").join(":");
		theform.eventArgument.value = eventArgument;
		send(theform);
	}

	function changeImg()
	{
		document.getElementById('valcodeImg').src='loginimg.jsp?id='+Math.random();
	}
	function changeImg2()
	{
		document.getElementById('valcodeImg2').src='loginimg2.jsp?id='+Math.random();
	}
	function on_return()
	{
		if(window.event.keyCode == 13){
			if (document.all('sub')!=null){
				// document.all('sub').click();
				$('#sub').click();
			}
		}
	}

	function submitForm()
{
	send('#form1');
}

function send(f)
	{
		var options = {
			dataType:"html",
			success: process
		};

		$(f).ajaxSubmit(options);
	}
	function process(m) {
	var arr = m.split("|");
	z=arr[0];
	//alert(z);
	if ( z == 200 )
	{
		self.location.href=arr[1];
	}
	else if(z == 301||z == 303){
		alert(v[z]);
		self.location.href='/win/develop_manage/app_list.jsp';
	}
	else if(z == 111){
		alert(v[z]);
		//test
	//	self.location.href='/win/login.jsp?return_url=687474703A2F2F6275792E73636C6F75646D2E636F6D2F60C00A7A7E';
		//zhengshi
		self.location.href='http://login.scloudm.com/scloudm_manage/login';
	}
	else
	{
		alert(v[z]);
		$('#submit').removeClass('loading');

	}
	}
