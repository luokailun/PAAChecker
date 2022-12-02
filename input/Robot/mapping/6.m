{
	"action": {

		"h_pickup": "pi(loc:room,obj:package)[!goal_in(obj,loc)& exists(loc1:room)[goal_in(obj,loc1)]?; pickup(obj,loc)]",
		"move_release": "pi(obj:package,loc1:room,loc2:room,d:roomdoor)[goal_in(obj,loc2)?; (open(loc1, loc2, d);move(loc1, loc2, d)#move(loc1, loc2, d));putdown(obj,loc2)]",
		"move_to_object": "pi(obj:package,loc1:room,loc2:room,d:roomdoor)[rloc(loc1)&!goal_in(obj,loc2)&in(obj,loc2)?; (open(loc1, loc2, d);move(loc1, loc2, d)#move(loc1, loc2, d))]"
	},

	"fluent": {
		"h_holding" : "exists(obj:package)[holding(obj)]",
		"pickable": "exists(obj:package,loc2:room, loc1:room)[rloc(loc1)&!goal_in(obj,loc1)& in(obj,loc1)&goal_in(obj,loc2)]",
		"movable":"exists(obj:package,l1:room,l2:room,d:roomdoor)[rloc(l1)&!goal_in(obj,l2)&in(obj,l2)&door(l1,l2,d)]",
		"success":"exists(obj:package,l1:room)[goal_in(obj,l1)&in(obj,l1)]"
	}
}

