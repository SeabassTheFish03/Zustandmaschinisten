from fa_manager import DFA_Manager

import json

def main():
    with open("fa_vault/simple.json", "r") as f:
        rawJson = json.loads(f.read())

    dfa_from_json = DFA_Manager.from_json(rawJson)
    print(dfa_from_json.dfa.states)

    dfa_from_dfa = DFA_Manager.from_dfa(dfa_from_json.dfa)
    print(dfa_from_dfa.dfa.states)

    dfa_from_mobj = DFA_Manager.from_mobj(dfa_from_dfa.mobj)
    print(dfa_from_mobj.dfa.states)

if __name__ == "__main__":
    main()
