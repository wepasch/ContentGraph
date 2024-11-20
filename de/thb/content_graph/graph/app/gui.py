import logging
import math
import tkinter as tk

from scipy.constants import golden as phi

from de.thb.content_graph.graph.node.disease import Disease
from de.thb.content_graph.graph.node.type import NodeType
from de.thb.content_graph.neo4j.neo4j_access import Neo4jAccess
from de.thb.misc.queryobjects import QueryNode
from de.thb.misc.util import setup_logging, get_resource

logger = logging.getLogger(__name__)

PATH_ICON: str = 'images/thb.ico'
NO_SELECTION: str = ''
WIDTH: int = 400
HEIGHT: int = math.ceil(phi * WIDTH)
WINDOW_GEO: str = f'{WIDTH}x{HEIGHT}'
FONT_MAIN: str = 'Comic Sans MS'
TITLE: str = 'Content Graph'


class GuiExplorer:
    __window: tk.Tk
    __disease_selection: tk.StringVar
    __disease_choice: Disease = None
    __access: Neo4jAccess

    def __init__(self):
        self.__window = meh()
        self.__disease_selection = tk.StringVar(self.__window)
        self.__disease_selection.set(NO_SELECTION)
        self.__access: Neo4jAccess = Neo4jAccess.get_access()
        selector: tk.OptionMenu = tk.OptionMenu(self.__window, self.__disease_selection,
                                                *map(lambda d: d.name,
                                                     self.__access.get_nodes_like(QueryNode('', NodeType.DISEASE))))
        selector.pack(fill=tk.BOTH, expand=True)
        ok_btn: tk.Button = tk.Button(self.__window, text='OK', font=(FONT_MAIN, 8), command=self.__eval_selection)
        ok_btn.pack()
        self.__window.mainloop()

    def __eval_selection(self) -> None:
        choice: str = self.__disease_selection.get()
        self.__disease_choice = next(filter(lambda d: choice == d.name,
                                            self.__access.get_nodes_like(QueryNode('', NodeType.DISEASE))),
                                     None)
        if choice == NO_SELECTION:
            logger.error(f'Selection of disease is empty (from \'{choice}\').')
            return
        logger.info(f'Chosen disease {self.__disease_choice.name}')
        self.__window.destroy()
        self.__window = meh()
        label: tk.Label = tk.Label(self.__window, text=self.__disease_choice.name)
        label.pack()

def meh() -> tk.Tk:
    frame: tk.Tk = tk.Tk()
    frame.geometry(WINDOW_GEO)
    frame.title(TITLE)
    frame.iconbitmap(get_resource(PATH_ICON))
    return frame


def main():
    ge: GuiExplorer = GuiExplorer()






if __name__ == "__main__":
    setup_logging()
    main()
