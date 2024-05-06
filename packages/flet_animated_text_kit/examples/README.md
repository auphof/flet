
# Development Build/Run and interactive testing

Terminal 1 - flet Animated Text Kit example1
```bash

# from flet dir
export FLET_VIEW_PATH=$HOME/dev/SANDBOX/SANDBOX-flet/modules/flet/client/build/linux/x64/debug/bundle
cd flet/packages/flet_animated_text_kit/examples/
FLET_FORCE_WEB_SERVER=true flet run example1.py  -p 8550
```
Terminal 2 - flet client (backend)
```bash
# from flet dir
cd flet/client
flutter run -d linux  --debug  -v
```

# Production Build

```bash
# Step 1 build
cd flet/client
flutter build linux  -v 

export FLET_VIEW_PATH=$HOME/dev/SANDBOX/SANDBOX-flet/modules/flet/client/build/linux/x64/release/bundle

# Step 2 Test
pushd flet/packages/flet_animated_text_kit/examples/
flet run  example1.py
popd
```