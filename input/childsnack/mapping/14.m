{
	"action": {
		
		"serve": "pi(c:child, t:tray, p2: place, s:sandwich, b:bread-portion, cont:content-portion)[make_sandwich_no_gluten(s,b,cont);put_on_tray(s,t);move_tray(t,kitchen,p2); !served(c)?;serve_sandwich_no_gluten(s,c,t,p2);move_tray(t,p2,kitchen)] # forall(c:child)[!allergic_gluten(c) or served(c)]?;nop()"
	},

	"fluent": {
		"servable":"exists(s:sandwich, b:bread-portion,cont:content-portion)[ no_gluten_bread(b)& no_gluten_content(cont)] | forall(c:child)[!allergic_gluten(c) or served(c)]"
	}
}

