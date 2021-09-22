function filterHolderNoIn()
{
	if (self.GetMoveParent().GetOwner() == activator)
		EntFireByHandle(self, "FireUser1", "", 0.0, activator, activator)
}
