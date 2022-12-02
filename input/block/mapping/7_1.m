{
	"action": {

		"onestep-move": "pi(x:block,y:block)[clear(x) & ! done(x) & goal_on(x,y) & done(y) & clear(y)?; ( pickup(x) #  pi(k:block)[unstack(x, k)]);stack(x, y)] # pi(x:block)[clear(x) & ! done(x) & ! on-table(x)?;pi(k: block)[unstack(x, k)]; putdown(x)] # pi(x:block)[on-table(x) & goal_on-table(x) | exists(y:block)[on(x,y) & goal_on(x,y) & done(y)]?;mark_done(x)] # forall(x:block)[done(x)]?;nop()"

	},

	"fluent": {

		"all-done": "exists(x:block,y:block)[clear(x) & !done(x) & goal_on(x,y) & done(y) & clear(y)]| exists(x:block)[clear(x) & !done(x) & !on-table(x)]| exists(x:block)[on-table(x) & goal_on-table(x) & !done(x)]| exists(x:block,y:block)[on(x,y) & goal_on(x,y) & done(y) & !done(x)]|forall(x:block)[done(x)]"
	}
}