'reach 0.1';
const shared = {
    showdeadline: Fun([UInt], Null)
}
export const main = Reach.App(() => {
    const Alice = Participant('Alice', {
        ...shared,
        Inheritance: Fun([], UInt),
        deadline: Fun([], UInt),
        presence: Fun([], UInt)
    })
    const Bob = Participant('Bob', {
        ...shared,
        acceptinheritance: Fun([UInt], Null),
    })

    init()
    Alice.only(() => {
        const payinherit = declassify(interact.Inheritance())
        const deadline_val = declassify(interact.deadline())
    })
    Alice.publish(payinherit, deadline_val)
        .pay(payinherit)
    commit()

    Bob.only(() => {
        const acceptinherit = declassify(interact.acceptinheritance(payinherit))
    })
    const stop = lastConsensusTime() + deadline_val
    Bob.publish(acceptinherit)
        .timeout(relativeTime(deadline_val), () => closeTo(Alice));
    var aliceanswer = 1
    invariant(balance() == payinherit)
    while (lastConsensusTime() <= stop) {
        commit()
        Alice.only(() => {
            const check_presence = declassify(interact.presence())
            const showdead = declassify(interact.showdeadline(deadline_val))
        })
        Alice.publish(check_presence, showdead)
        commit()
        Bob.only(() => {
            const showdead2 = declassify(interact.showdeadline(deadline_val))
        })
        Bob.publish(showdead2)
        aliceanswer = check_presence
        continue
    }

    transfer(payinherit).to(aliceanswer == 1 ? Alice : Bob)
    commit()

});
