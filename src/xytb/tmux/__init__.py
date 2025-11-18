"""
Tmux toolkit based on libtmux, with a simple, user-friendly API.

Features:

.. code-block:: python

    pane = T("<session name>.<window name>")  # defaults to pane 0
    pane.r("ls")  # run command 'ls' in the pane (sends Enter)

This module provides:

- T(target): returns a TmuxPane bound to the given target string.
- TmuxPane.r(cmd): sends a command to the pane via tmux (using send-keys).

Target format:

- "<session>.<window>"           -> pane index 0
- "<session>.<window>.<pane>"    -> explicit pane index

Exceptions:

- ValueError is raised if the target cannot be resolved.
"""
from __future__ import annotations

from typing import Tuple
from loguru import logger
import time
import libtmux
from libtmux._internal.query_list import ObjectDoesNotExist


__all__ = ["TmuxPane", "T"]


class TmuxPane:
    """
    Lightweight wrapper over libtmux Pane providing a friendly run method.

    Attributes:
        pane (libtmux.Pane): The underlying libtmux pane instance.
    """

    def __init__(self, pane: "libtmux.Pane") -> None:
        self.pane = pane

    def r(self, cmd: str, enter: bool = True, wait=True) -> None:
        """
        Run a command in the pane by sending keys.

        Args:
            cmd: The command string to send to the pane.
            enter: Whether to send Enter after the command (default: True).
        """
        # libtmux Pane.send_keys will send the given keys to the pane.
        # Using enter=True sends Enter after the keys.
        done_marker = "__tmux_done__"
        echo_cmd_suffix = f"; echo {done_marker}"
        cmd = f"{cmd} {echo_cmd_suffix}"
        logger.info(f"Sending command {cmd!r} to pane {self.pane.session_name}.{self.pane.window.name}.{self.pane.pane_index}")
        self.pane.send_keys(cmd, enter=enter)

        time.sleep(1 + len(cmd) / 80)  # NOTE: it is very important to sleep here. Make sure the marker has been sent!

        # If we executed the command (enter=True), wait until the marker shows up in output.
        if wait:
            while True:
                lines = self.pane.capture_pane()  # why it only return 

                last_line = ""
                for line in lines[::-1]:
                    # latest line is finished
                    # Assumption: the echo result will appear in one line.
                    if done_marker == line.strip():
                        return

                    # latest line is not finished
                    # Assumption: the command will not be split into more than 2 lines.!!!
                    if done_marker in (line + last_line):
                        break
                    last_line = line

                time.sleep(0.1)

    def __repr__(self) -> str:  # pragma: no cover
        pane_id = getattr(self.pane, "pane_id", "?")
        return f"<TmuxPane id={pane_id!r}>"


def _parse_target(target: str) -> Tuple[str, str, int]:
    """
    Parse a target string of the format:
        "<session>.<window>" or "<session>.<window>.<pane>"

    Returns:
        (session_name, window_name, pane_index)

    Raises:
        ValueError: If the format is invalid or pane index is not an integer.
    """
    parts = target.split(".")
    if len(parts) not in (2, 3):
        raise ValueError(
            f"Invalid target format {target!r}. Expected '<session>.<window>' or '<session>.<window>.<pane>'."
        )

    session_name, window_name = parts[0], parts[1]
    pane_index = 0
    if len(parts) == 3:
        try:
            pane_index = int(parts[2])
        except ValueError as e:
            raise ValueError(
                f"Invalid pane index {parts[2]!r} in target {target!r}."
            ) from e

    return session_name, window_name, pane_index


def T(target: str, create_if_not_exists: bool = False) -> TmuxPane:
    """
    Resolve a tmux target and return a TmuxPane wrapper.

    Args:
        target: Target string "<session>.<window>" or "<session>.<window>.<pane>".
        create_if_not_exists: When True, create the session/window/pane if missing.

    Returns:
        TmuxPane bound to the resolved pane.

    Raises:
        ValueError: If session, window, or pane cannot be found (and create_if_not_exists is False).
    """
    session_name, window_name, pane_index = _parse_target(target)

    server = libtmux.Server()
    # 1) try to find the session
    try:
        session = server.sessions.get(session_name=session_name)
    except ObjectDoesNotExist:
        if create_if_not_exists:
            session = server.new_session(session_name=session_name, attach=False)
            # Use the auto-created window; rename it to requested window_name to avoid creating an extra window.
            win = session.windows[0]
            if win.name != window_name:
                win.rename_window(window_name)
        else:
            raise

    # 2) try to find the window
    # 2.1) try to find the window by name
    try:
        window = session.windows.get(window_name=window_name)
    except ObjectDoesNotExist:
        window = None

    # 2.2) try to find the window by index
    if window is None:
        # Fallback: allow numeric window index if name not found
        try:
            win_idx = int(window_name)
            try:
                window = session.windows.get(window_index=win_idx)
            except ObjectDoesNotExist:
                window = None
        except ValueError:
            window = None

    # 2.3) create the window if not found
    if window is None:
        if create_if_not_exists:
            window = session.new_window(attach=False, window_name=window_name)
        else:
            raise ObjectDoesNotExist

    # 3) find the pane
    panes = window.panes
    if pane_index < 0:
        raise ValueError(
            f"Pane index {pane_index} out of range for window {window_name!r} in session {session_name!r} "
            f"(available panes: {len(panes)})."
        )

    # 3.1) create enough panes
    while pane_index >= len(panes):
        if create_if_not_exists:
            window.split_window(attach=False)
            panes = window.panes
        else:
            raise ObjectDoesNotExist

    # 3.2) return the pane via index.
    pane = panes[pane_index]
    return TmuxPane(pane)
