## The Observer Pattern
> also sometimes called the listener

all code, text and ideas from https://youtu.be/oNalXg67XEE
original code copied from https://github.com/arjancodes/betterpython

>The Observer Design Pattern deals with One-to-Many relationships and utilizes events to let subscribed entities know about changes in an observable.
>The source of these events is called the subject or observable which sends events as streams. The observers or sinks can subscribe to the observable to obtain the events. The observable keeps track of the list of observers and notifies them of the changes when the state of the observable changes.
Source: https://stackabuse.com/observer-design-pattern-in-python/

The important thing to remember is that there are two roles: The subject and the observer.
The Subject does things and changes things and notifies the observer that it happened.
Events are a variant of the observer / listener design pattern.
Event systems are a good example of a design that results in code with **low coupling** and **strong cohesion.**

In the after code we can see that imports are cleaner and more organized. The only dependency is on the event system. Also methods have become much shorter.
