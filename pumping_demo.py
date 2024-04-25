import sys
import json

from manim import *
from utils import *
from labeledEdgeDiGraph import LabeledEdgeDiGraph

class Pumping_Demo(Scene):
    def __init__(self, rawJson):
        super().__init__()
        self.rawJson = rawJson

        self.nfa = JSONToDFA(rawJson)

        self.mobj = FAToMobj(self.nfa).shift(3*RIGHT)

        self.checklist = BulletedList(
            "State the claim",
            "Indicate type of proof",
            "Assume to the contrary",
            "Identify p",
            "Choose a string L, which has length at least p",
            "Observe the pumping lemma holds",
            "Use the rules to identify xyz",
            "Choose the number of times to pump",
            "Prove the contradiction",
            font_size = 24,
        ).shift(3*LEFT)

        self.right = VGroup()

    def anim_init(self):
        return [Create(self.checklist)]

    def anim_step1(self):
        self.right = Tex("We claim the language $L = 0^n 1^n$\\\\is not regular because the intention of the pumping lemma for regular languages is to assert that $L$ is not accepted by any DFA, which means it is not regular", font_size=24).shift(3*RIGHT)
        anims = [Indicate(self.checklist[0]), FadeIn(self.right)]
        return anims

    def anim_step2(self):
        new_right = Tex("We will do so using contradiction,\\\\via the Pumping Lemma for regular languages", font_size=24).shift(3*RIGHT)
        self.remove(self.right)
        anims = [Indicate(self.checklist[1]), FadeIn(new_right)]
        self.right = new_right
        return anims

    def anim_step3(self):
        new_right = Tex("Assume to the contrary there exists some arbitrary DFA $M$\\\\that has a language of $0^n 1^n$.", font_size=24).shift(3*RIGHT).shift(UP)
        self.mobj = self.mobj.shift(2*DOWN).scale(0.5)
        self.remove(self.right)
        anims = [Indicate(self.checklist[2]), Create(self.mobj)]
        self.right = new_right
        return anims

    def anim_step4(self):
        desc = Tex("Let $p$ be the number of states of $M$. For simplicity, we have illustrated\\\\ a DFA with 3 states, but it could be any finite number.", font_size=24).shift(3*RIGHT).shift(UP)
        self.remove(self.right)
        anims = [Indicate(self.checklist[3]), FadeIn(desc)]
        self.right = desc
        return anims

    def anim_step5(self):
        desc = Tex("Choose the string $w$ using the format $0^p 1^p$.\\\\This guarantees $w$ has a length of at least $p$\\\\and that there are $p$ $0$s, which will\\\\become important later", font_size=24).shift(3*RIGHT).shift(2.5*UP)
        self.l = Tex("$000111$", font_size=24, color="yellow").shift(3*RIGHT).shift(UP)
        self.remove(self.right)
        anims = [Indicate(self.checklist[4]), ReplacementTransform(self.right, desc), Create(self.l)]
        self.right = desc
        return anims

    def anim_step6(self):
        desc = Tex("We next observe and state that the pumping lemma for regular languages holds for this string. $w$ is an element of the language of $L$ by definition, and it has a length greater than $p$. Therefore the pumping lemma holds for $w$", font_size=24).shift(3*RIGHT).shift(2.5*UP)
        self.l = Tex("$000111$", font_size=24, color="yellow").shift(3*RIGHT).shift(UP)
        self.remove(self.right)
        anims = [Indicate(self.checklist[5]), ReplacementTransform(self.right, desc), Create(self.l)]
        self.right = desc
        return anims

    def anim_step7(self):
        desc = Tex("We next use the pumping lemma rule to identify the different decompositions of $w$ into $x$, $y$, and $z$. We need to determine that all valid possibilities of how $w$ could be split will still break out of the language", font_size=24).shift(3*RIGHT).shift(2.5*UP)
        self.l = Tex("$000111$", font_size=24, color="yellow").shift(3*RIGHT).shift(UP)
        self.remove(self.right)
        self.right = desc
        return [Indicate(self.checklist[6]), ReplacementTransform(self.l, MathTex("""x=0^\\alpha, y=0^\\beta, z=1^{p - \\alpha - \\beta}""", font_size=24, color="yellow").move_to(self.l))]

    def anim_step8(self):
        self.remove(self.l)
        self.play(Create(Tex("Let $i = 2$", font_size=24, color="red").move_to(self.l).shift(0.5*UP)))
        self.play(Indicate(self.checklist[7]), ShowPassingFlash(self.mobj.edges[('q0', 'q1')].copy()), ReplacementTransform(self.l, MathTex("""y=0^\\beta, z=1^{p-\\alpha-\\beta}""", font_size=24, color="yellow").move_to(self.l)))
        self.remove(self.l)
        self.wait(0.5)

        self.play(ShowPassingFlash(self.mobj.edges[('q1', 'q1')].copy()))
        self.play(ShowPassingFlash(self.mobj.edges[('q1', 'q1')].copy()))

        return [ShowPassingFlash(self.mobj.edges[('q1', 'q2')].copy()), Uncreate(self.l)]

    def anim_step9(self):
        self.remove(self.l)
        
        return [Indicate(self.checklist[8])]

    def construct(self):
        self.play(*self.anim_init())
        self.wait()
        self.play(*self.anim_step1())
        self.wait()
        self.play(*self.anim_step2())
        self.wait()
        self.play(*self.anim_step3())
        self.wait()
        self.play(*self.anim_step4())
        self.wait()
        self.play(*self.anim_step5())
        self.wait()
        self.play(*self.anim_step6())
        self.wait()
        self.play(*self.anim_step7())
        self.wait()
        self.play(*self.anim_step8())
        self.wait()
        self.play(*self.anim_step9())
        self.wait()

def main(args):
    if len(sys.argv) == 2 or len(sys.argv) == 3:
        dfaFilename = sys.argv[1]
        if len(sys.argv) == 3:
            picture_quality = sys.argv[2]
        else:
            picture_quality = "medium_quality"
    else:
        print("Usage: python pumping_demo.py <DFA.json> [picture_quality (default low)]")
        exit(code=2)

    with open(dfaFilename, "r") as f:
        rawJson = json.loads(f.read())

    with tempconfig({"quality": picture_quality, "preview": True}):
        scene = Pumping_Demo(rawJson)
        scene.render()

if __name__ == "__main__":
    main(sys.argv)
