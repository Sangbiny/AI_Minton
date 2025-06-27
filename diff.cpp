40c40
<             if (result.size() < 4)
---
>             if (result.size() < 4 && p->getStates() != currentGameIndex - 1)
55c55,56
<                 if (existingStates.find(p->getStates()) == existingStates.end())
---
>                 if (existingStates.find(p->getStates()) == existingStates.end() &&
>                     p->getStates() != currentGameIndex - 1)
87a89
> 
