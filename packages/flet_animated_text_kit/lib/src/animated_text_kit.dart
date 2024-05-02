import 'dart:async';
import 'dart:convert';

import 'package:flet/flet.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/widgets.dart';
import 'package:animated_text_kit/animated_text_kit.dart';

import 'package:flet/src/utils/text.dart';
// import 'package:flet/src/utils/theme.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

class AnimatedTextKitControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;
  final bool? parentAdaptive;
  final Widget? nextChild;
  final FletControlBackend backend;

  const AnimatedTextKitControl(
      {super.key,
      required this.parent,
      required this.control,
      required this.children,
      required this.nextChild,
      required this.parentDisabled,
      required this.parentAdaptive,
      required this.backend});

  @override
  State<AnimatedTextKitControl> createState() => _AnimatedTextKitControlState();
}

class _AnimatedTextKitControlState extends State<AnimatedTextKitControl>
    with FletStoreMixin {
  String _text = "";
  // bool _revealPassword = false;
  bool _focused = false;
  // late TextEditingController _controller;
  late final FocusNode _focusNode;
  late final FocusNode _shiftEnterfocusNode;
  String? _lastFocusValue;
  @override
  void initState() {
    super.initState();
    // _controller = TextEditingController();
    _shiftEnterfocusNode = FocusNode(
      onKeyEvent: (FocusNode node, KeyEvent evt) {
        if (!HardwareKeyboard.instance.isShiftPressed &&
            evt.logicalKey.keyLabel == 'Enter') {
          if (evt is KeyDownEvent) {
            widget.backend.triggerControlEvent(widget.control.id, "submit");
          }
          return KeyEventResult.handled;
        } else {
          return KeyEventResult.ignored;
        }
      },
    );
    _shiftEnterfocusNode.addListener(_onShiftEnterFocusChange);
    _focusNode = FocusNode();
    _focusNode.addListener(_onFocusChange);
  }

  @override
  void dispose() {
    // _controller.dispose();
    _shiftEnterfocusNode.removeListener(_onShiftEnterFocusChange);
    _shiftEnterfocusNode.dispose();
    _focusNode.removeListener(_onFocusChange);
    _focusNode.dispose();
    super.dispose();
  }

  void _onShiftEnterFocusChange() {
    setState(() {
      _focused = _shiftEnterfocusNode.hasFocus;
    });
    widget.backend.triggerControlEvent(widget.control.id,
        _shiftEnterfocusNode.hasFocus ? "focus" : "blur", "");
  }

  void _onFocusChange() {
    setState(() {
      _focused = _focusNode.hasFocus;
    });
    widget.backend.triggerControlEvent(
        widget.control.id, _focusNode.hasFocus ? "focus" : "blur", "");
  }

  @override
  Widget build(BuildContext context) {
    debugPrint(
        "AnimatedTextKit build: ${widget.control.id} (${widget.control.hashCode})");
    return withPagePlatform((context, platform) {
      bool autofocus = widget.control.attrBool("autofocus", false)!;
      bool disabled = widget.control.isDisabled || widget.parentDisabled;

      bool? adaptive =
          widget.control.attrBool("adaptive") ?? widget.parentAdaptive;
      // if (adaptive == true &&
      //     (platform == TargetPlatform.iOS ||
      //         platform == TargetPlatform.macOS)) {
      //   return CupertinoTextFieldControl(
      //       control: widget.control,
      //       children: widget.children,
      //       parent: widget.parent,
      //       parentDisabled: widget.parentDisabled,
      //       parentAdaptive: adaptive,
      //       backend: widget.backend);
      // }

      // bool disabled = control.isDisabled || parentDisabled;
      // var src = widget.control.attrString("src", "")!;
      // var srcBase64 = widget.control.attrString("srcBase64", "")!;

      debugPrint("AnimatedTextKit attrString: ${widget.control} ");

      // var text = widget.control.attrString("text",
      //     "text appears to be blank,  so I will just say... Hello world!")!;
      String text = widget.control.attrs["text"] ??
          "text appears to be blank,  so I will just say... Hello world!";
      if (_text != text) {
        _text = text;
        // _controller.text = text;
      }

      // var prefixControls =
      //     widget.children.where((c) => c.name == "prefix" && c.isVisible);
      // var suffixControls =
      //     widget.children.where((c) => c.name == "suffix" && c.isVisible);

      var cursorColor = widget.control.attrColor("cursorColor", context);
      var selectionColor = widget.control.attrColor("selectionColor", context);

      var textSize = widget.control.attrDouble("textSize");

      var color = widget.control.attrColor("color", context);
      var focusedColor = widget.control.attrColor("focusedColor", context);

      var theme = Theme.of(context);

      var textStyleTest = widget.control.attrString("textStyle");
      debugPrint("AnimatedTextKit textStyleTest: ${textStyleTest} ");
      TextStyle? textStyle = parseTextStyle(theme, widget.control, "textStyle");
      // TextStyle? textStyle = TextStyle(
      //   fontSize: 32.0,
      //   fontWeight: FontWeight.bold,
      // );
      debugPrint("AnimatedTextKit textStyle: ${textStyle} ");

      if (textSize != null || color != null || focusedColor != null) {
        textStyle = (textStyle ?? const TextStyle()).copyWith(
            fontSize: textSize,
            color: _focused ? focusedColor ?? color : color);
      }
      debugPrint("AnimatedTextKit style: ${textStyle} ");
      debugPrint("AnimatedTextKit text: ${text} ");

      // if (text == "") {
      //   return const ErrorControl(
      //       "AnimatedTextKit must have \"text\"  specified.");
      // }

      var repeatForever =
          widget.control.attrBool("repeat_forever", true) ?? true;
      var speed = widget.control.attrInt("speed", 250) ?? 250;
      var pause = widget.control.attrInt("pause", 1000) ?? 1000;

      var displayFullTextOnTap =
          widget.control.attrBool("display_full_text_on_tap", false) ?? false;
      var stopPauseOnTap =
          widget.control.attrBool("stop_pause_on_tap", false) ?? false;
      var isRepeatingAnimation =
          widget.control.attrBool("is_repeating_animation", true) ?? true;
      var totalRepeatCount =
          widget.control.attrInt("total_repeat_count", 0) ?? 0;
      // var backgroundLoading = widget.control.attrBool("backgroundLoading");
      // var reverse = widget.control.attrBool("reverse");
      // var animate = widget.control.attrBool("animate");
      // var fit = parseBoxFit(widget.control, "fit");
      // FilterQuality filterQuality = FilterQuality.values.firstWhere((e) =>
      //     e.name.toLowerCase() ==
      //     widget.control.attrString("filterQuality", "low")!.toLowerCase());

      void onWarning(String value) {
        if (widget.control.attrBool("onError", false)!) {
          widget.backend.triggerControlEvent(widget.control.id, "error", value);
        }
      }

      bool shiftEnter = widget.control.attrBool("shiftEnter", false)!;
      FocusNode focusNode = shiftEnter ? _shiftEnterfocusNode : _focusNode;
      var focusValue = widget.control.attrString("focus");
      if (focusValue != null && focusValue != _lastFocusValue) {
        _lastFocusValue = focusValue;
        focusNode.requestFocus();
      }
      Widget animatedTextKit = AnimatedTextKit(
        // autofocus: autofocus,
        // enabled: !disabled,
        animatedTexts: [
          TypewriterAnimatedText(
            text,
            textStyle: textStyle,
            // textStyle: const TextStyle(
            //   fontSize: 32.0,
            //   fontWeight: FontWeight.bold,
            // ),
            speed: Duration(milliseconds: speed),
          ),
        ],
        isRepeatingAnimation: isRepeatingAnimation,
        repeatForever: repeatForever,
        totalRepeatCount: totalRepeatCount,
        pause: Duration(milliseconds: pause),
        displayFullTextOnTap: displayFullTextOnTap,
        stopPauseOnTap: stopPauseOnTap,
        onTap: () {
          debugPrint("AnimatedTextKit ${widget.control.id} onTap!");
          widget.backend.triggerControlEvent(widget.control.id, "on_tap");
        },
        onFinished: () {
          debugPrint("AnimatedTextKit ${widget.control.id} onFinished!");
          widget.backend.triggerControlEvent(widget.control.id, "on_finished");
        },
        onNext: (int, bool) {
          debugPrint("AnimatedTextKit ${widget.control.id} onNext!");
          widget.backend.triggerControlEvent(widget.control.id, "on_next");
        },
        onNextBeforePause: (int, bool) {
          debugPrint("AnimatedTextKit ${widget.control.id} onNextBeforePause!");
          widget.backend
              .triggerControlEvent(widget.control.id, "on_next_before_pause");
        },
      );

      if (cursorColor != null || selectionColor != null) {
        animatedTextKit = TextSelectionTheme(
            data: TextSelectionTheme.of(context).copyWith(
                cursorColor: cursorColor, selectionColor: selectionColor),
            child: animatedTextKit);
      }

      if (widget.control.attrInt("expand", 0)! > 0) {
        return constrainedControl(
            context, animatedTextKit, widget.parent, widget.control);
      } else {
        return LayoutBuilder(
          builder: (BuildContext context, BoxConstraints constraints) {
            if (constraints.maxWidth == double.infinity &&
                widget.control.attrDouble("width") == null) {
              animatedTextKit = ConstrainedBox(
                constraints: const BoxConstraints.tightFor(width: 300),
                child: animatedTextKit,
              );
            }

            return constrainedControl(
                context, animatedTextKit, widget.parent, widget.control);
          },
        );
        // return withPageArgs((context, pageArgs) {
        //   Widget? animatedTextKit;
        //   return constrainedControl(
        //       context, animatedTextKit, widget.parent, widget.control);
        // });
      }
    });
  }
}