export default function getNumberOfAttacks(username, data) {
    let numberOfAttacks = 0;
    for (let attack of data.attacks) {
        if (attack === username) numberOfAttacks++;
    }
    return numberOfAttacks;
}